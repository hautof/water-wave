from typing import List, Dict, Any
from ..core.agent import Agent
from ..messages.base import Message, MessageType
from ..core.state import SystemState, Task

class AnalystAgent(Agent):
    """Analyst agent for requirement analysis and task planning"""
    
    def __init__(self, agent_id: str = "analyst", name: str = "Analyst Agent"):
        super().__init__(agent_id, name)
    
    def get_capabilities(self) -> List[str]:
        return [
            "requirement_analysis",
            "task_decomposition",
            "strategy_planning"
        ]
    
    def validate_input(self, message: Message) -> bool:
        # Validate input message format
        return message.message_type in [MessageType.USER_REQUEST, MessageType.TASK_FEEDBACK, MessageType.VALIDATION_RESULT]
    
    async def process_message(self, message: Message, state: SystemState) -> List[Message]:
        # Process message and return response messages
        if not self.validate_input(message):
            raise ValueError("Invalid input message format")
        
        # Process based on message type
        if message.message_type == MessageType.USER_REQUEST:
            return self._analyze_request(message, state)
        elif message.message_type == MessageType.TASK_FEEDBACK:
            return self._handle_feedback(message, state)
        elif message.message_type == MessageType.VALIDATION_RESULT:
            return self._handle_validation_result(message, state)
        
        # Return empty list if no specific processing is needed
        return []
    
    def _analyze_request(self, message: Message, state: SystemState) -> List[Message]:
        """Analyze user request and generate task plan"""
        # Extract request details
        request_text = message.payload.get("text", "")
        
        # In a full implementation, this would contain the logic for:
        # 1. Requirement complexity assessment
        # 2. Task decomposition algorithm
        # 3. Dependency analysis
        # 4. Risk assessment
        
        # For this implementation, we'll create a simplified task plan
        task_plan = self._create_task_plan(request_text)
        
        # Create task plan message
        plan_message = Message(
            id=f"plan_{message.id}",
            sender_id=self.agent_id,
            receiver_id="executor",
            message_type=MessageType.TASK_PLAN,
            payload={
                "plan": task_plan,
                "original_request": request_text
            },
            correlation_id=message.correlation_id
        )
        
        return [plan_message]
    
    def _handle_feedback(self, message: Message, state: SystemState) -> List[Message]:
        """Handle task feedback and adjust plan if needed"""
        # Extract feedback details
        feedback = message.payload.get("feedback", "")
        task_id = message.payload.get("task_id", "")
        
        # In a full implementation, this would contain the logic for:
        # 1. Analyzing feedback
        # 2. Adjusting task plan
        # 3. Re-prioritizing tasks
        # 4. Re-allocating resources
        
        # For this implementation, we'll create a simplified response
        response_message = Message(
            id=f"response_{message.id}",
            sender_id=self.agent_id,
            receiver_id=message.sender_id,
            message_type=MessageType.TASK_PLAN,
            payload={
                "feedback_response": f"Received feedback: {feedback}",
                "adjusted_plan": "Plan adjusted based on feedback"
            },
            correlation_id=message.correlation_id
        )
        
        return [response_message]
    
    def _handle_validation_result(self, message: Message, state: SystemState) -> List[Message]:
        """Handle validation results and decide on next steps"""
        # Extract validation result
        is_valid = message.payload.get("is_valid", False)
        validation_notes = message.payload.get("notes", "")
        
        # If validation failed, we need to re-plan
        if not is_valid:
            original_request = state.execution_context.get("original_request", "")
            
            # Create a new task plan based on validation feedback
            task_plan = self._create_task_plan(original_request, validation_notes)
            
            # Create new task plan message
            plan_message = Message(
                id=f"replan_{message.id}",
                sender_id=self.agent_id,
                receiver_id="executor",
                message_type=MessageType.TASK_PLAN,
                payload={
                    "plan": task_plan,
                    "original_request": original_request,
                    "validation_feedback": validation_notes
                },
                correlation_id=message.correlation_id
            )
            
            return [plan_message]
        
        # If validation passed, no further action needed from analyst
        return []
    
    def _create_task_plan(self, request_text: str, feedback: str = "") -> Dict[str, Any]:
        """Create a task plan based on request and optional feedback"""
        # In a full implementation, this would contain the logic for:
        # 1. Detailed task breakdown
        # 2. Resource allocation
        # 3. Timeline estimation
        # 4. Dependency mapping
        
        # For this implementation, we'll create a simplified plan
        plan = {
            "tasks": [
                {
                    "task_id": "1",
                    "name": "Task 1",
                    "description": f"First task for: {request_text}",
                    "dependencies": [],
                    "priority": 1
                },
                {
                    "task_id": "2",
                    "name": "Task 2",
                    "description": f"Second task for: {request_text}",
                    "dependencies": ["1"],
                    "priority": 2
                }
            ],
            "strategy": "Sequential execution",
            "feedback_incorporated": feedback if feedback else "None"
        }
        
        return plan
