from typing import Dict, Any, Callable
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from ..agents.analyst import AnalystAgent
from ..agents.executor import ExecutorAgent
from ..agents.validator import ValidatorAgent
from ..core.state import SystemState
from ..messages.base import Message, MessageType

class MultiAgentWorkflow:
    """LangGraph workflow for multi-agent collaboration"""
    
    def __init__(self):
        self.analyst = AnalystAgent()
        self.executor = ExecutorAgent()
        self.validator = ValidatorAgent()
        self.graph = self._create_graph()
    
    def _create_graph(self) -> StateGraph:
        """Create and configure the LangGraph workflow"""
        graph = StateGraph(SystemState)
        
        # Add agent nodes
        graph.add_node("analyst", self._analyst_node)
        graph.add_node("executor", self._executor_node)
        graph.add_node("validator", self._validator_node)
        
        # Add edges
        graph.add_edge("analyst", "executor")
        graph.add_edge("executor", "validator")
        
        # Add conditional edges for retry logic
        graph.add_conditional_edges(
            "validator",
            self._should_retry,
            {
                "retry": "analyst",
                "complete": END
            }
        )
        
        # Set entry point
        graph.set_entry_point("analyst")
        
        # Compile with checkpointer
        return graph.compile(checkpointer=MemorySaver())
    
    async def _analyst_node(self, state: SystemState) -> Dict[str, Any]:
        """Analyst agent node function"""
        # Get the initial message or feedback
        # For now, we'll need to get this from the state attributes
        # In a more complete implementation, we might pass this differently
        message = getattr(state, 'current_message', None)
        if not message:
            raise ValueError("No message provided to analyst node")
        
        # Process the message
        response_messages = await self.analyst.process_message(message, state)
        
        # Update state
        state.message_history.append(message)
        for response in response_messages:
            state.message_history.append(response)
        
        # Return updated state
        return {
            "messages": response_messages
        }
    
    async def _executor_node(self, state: SystemState) -> Dict[str, Any]:
        """Executor agent node function"""
        # Get messages to process
        messages = getattr(state, 'messages', [])
        if not messages:
            raise ValueError("No messages provided to executor node")
        
        # Process each message
        all_response_messages = []
        for message in messages:
            response_messages = await self.executor.process_message(message, state)
            all_response_messages.extend(response_messages)
        
        # Update state
        for message in messages:
            state.message_history.append(message)
        for response in all_response_messages:
            state.message_history.append(response)
        
        # Return updated state
        return {
            "messages": all_response_messages
        }
    
    async def _validator_node(self, state: SystemState) -> Dict[str, Any]:
        """Validator agent node function"""
        # Get messages to process
        messages = getattr(state, 'messages', [])
        if not messages:
            raise ValueError("No messages provided to validator node")
        
        # Process each message
        all_response_messages = []
        for message in messages:
            response_messages = await self.validator.process_message(message, state)
            all_response_messages.extend(response_messages)
        
        # Update state
        for message in messages:
            state.message_history.append(message)
        for response in all_response_messages:
            state.message_history.append(response)
        
        # Return updated state
        return {
            "messages": all_response_messages
        }
    
    def _should_retry(self, state: SystemState) -> str:
        """Decision function for retry logic"""
        # Get messages from the state
        messages = getattr(state, 'messages', [])
        
        # Check if any validation result indicates failure
        for message in messages:
            if message.message_type == MessageType.VALIDATION_RESULT:
                is_valid = message.payload.get("is_valid", True)
                if not is_valid:
                    # Check retry count to prevent infinite loops
                    if state.retry_count < 3:  # Max 3 retries
                        state.retry_count += 1
                        return "retry"
        
        # If no retry needed, complete the workflow
        return "complete"
    
    async def run(self, initial_message: Message, session_id: str = None) -> SystemState:
        """Run the workflow with an initial message"""
        # Create initial state
        initial_state = SystemState(
            session_id=session_id or "default_session",
            user_id="cli_user"
        )
        initial_state.current_message = initial_message
        
        # Configure checkpointer if session_id is provided
        config = {"configurable": {"thread_id": session_id}} if session_id else {}
        
        # Run the graph
        final_state = await self.graph.ainvoke({"__root__": initial_state, "current_message": initial_message}, config)
        
        # Extract the actual SystemState from the returned dict if needed
        if isinstance(final_state, dict) and "__root__" in final_state:
            final_state = final_state["__root__"]
        elif isinstance(final_state, dict):
            # Create a new SystemState from the returned dict
            final_state = SystemState(**final_state)
        
        return final_state