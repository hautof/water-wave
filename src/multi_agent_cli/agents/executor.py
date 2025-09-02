from typing import List, Dict, Any
from ..core.agent import Agent
from ..messages.base import Message, MessageType
from ..core.state import SystemState, Task

class ExecutorAgent(Agent):
    """Executor agent for task execution and tool invocation"""
    
    def __init__(self, agent_id: str = "executor", name: str = "Executor Agent"):
        super().__init__(agent_id, name)
    
    def get_capabilities(self) -> List[str]:
        return [
            "command_execution",
            "file_operations",
            "api_calls"
        ]
    
    def validate_input(self, message: Message) -> bool:
        # Validate input message format
        return message.message_type in [MessageType.TASK_PLAN, MessageType.EXECUTION_COMMAND, MessageType.RETRY_REQUEST]
    
    async def process_message(self, message: Message, state: SystemState) -> List[Message]:
        # Process message and return response messages
        if not self.validate_input(message):
            raise ValueError("Invalid input message format")
        
        # Process based on message type
        if message.message_type == MessageType.TASK_PLAN:
            return self._execute_task_plan(message, state)
        elif message.message_type == MessageType.EXECUTION_COMMAND:
            return self._execute_command(message, state)
        elif message.message_type == MessageType.RETRY_REQUEST:
            return self._handle_retry_request(message, state)
        
        # Return empty list if no specific processing is needed
        return []
    
    def _execute_task_plan(self, message: Message, state: SystemState) -> List[Message]:
        """Execute a task plan and return results"""
        # Extract plan details
        plan = message.payload.get("plan", {})
        tasks = plan.get("tasks", [])
        
        # In a full implementation, this would contain the logic for:
        # 1. Task queue management
        # 2. Concurrent execution control
        # 3. Exception handling mechanism
        # 4. Result collection and organization
        
        # For this implementation, we'll simulate execution
        execution_results = []
        for task in tasks:
            result = self._simulate_task_execution(task)
            execution_results.append(result)
        
        # Create execution result message
        result_message = Message(
            id=f"result_{message.id}",
            sender_id=self.agent_id,
            receiver_id="validator",
            message_type=MessageType.EXECUTION_RESULT,
            payload={
                "results": execution_results,
                "plan": plan
            },
            correlation_id=message.correlation_id
        )
        
        return [result_message]
    
    def _execute_command(self, message: Message, state: SystemState) -> List[Message]:
        """Execute a specific command"""
        # Extract command details
        command = message.payload.get("command", "")
        
        # In a full implementation, this would contain the logic for:
        # 1. Command parsing and validation
        # 2. Tool invocation
        # 3. Progress monitoring
        # 4. Error handling
        
        # For this implementation, we'll simulate command execution
        result = self._simulate_command_execution(command)
        
        # Create execution result message
        result_message = Message(
            id=f"cmd_result_{message.id}",
            sender_id=self.agent_id,
            receiver_id=message.sender_id,
            message_type=MessageType.EXECUTION_RESULT,
            payload={
                "command": command,
                "result": result
            },
            correlation_id=message.correlation_id
        )
        
        return [result_message]
    
    def _handle_retry_request(self, message: Message, state: SystemState) -> List[Message]:
        """Handle retry requests for failed tasks"""
        # Extract retry details
        task_id = message.payload.get("task_id", "")
        error_info = message.payload.get("error", "")
        
        # In a full implementation, this would contain the logic for:
        # 1. Analyzing error information
        # 2. Adjusting execution parameters
        # 3. Re-executing task
        # 4. Implementing retry limits
        
        # For this implementation, we'll simulate retry
        retry_result = self._simulate_retry_execution(task_id, error_info)
        
        # Create execution result message
        result_message = Message(
            id=f"retry_result_{message.id}",
            sender_id=self.agent_id,
            receiver_id="validator",
            message_type=MessageType.EXECUTION_RESULT,
            payload={
                "task_id": task_id,
                "retry_result": retry_result,
                "retry_attempt": True
            },
            correlation_id=message.correlation_id
        )
        
        return [result_message]
    
    def _simulate_task_execution(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate task execution (placeholder for actual implementation)"""
        # In a full implementation, this would actually execute the task
        return {
            "task_id": task.get("task_id"),
            "status": "completed",
            "result": f"Executed task: {task.get('name')}",
            "execution_time": 0.1
        }
    
    def _simulate_command_execution(self, command: str) -> str:
        """Simulate command execution (placeholder for actual implementation)"""
        # In a full implementation, this would actually execute the command
        return f"Executed command: {command}"
    
    def _simulate_retry_execution(self, task_id: str, error_info: str) -> Dict[str, Any]:
        """Simulate retry execution (placeholder for actual implementation)"""
        # In a full implementation, this would actually retry the task
        return {
            "task_id": task_id,
            "status": "completed_after_retry",
            "result": f"Retried task {task_id} after error: {error_info}",
            "retry_count": 1
        }
