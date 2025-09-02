import unittest
from datetime import datetime
from multi_agent_cli.messages.base import Message, MessageType
from multi_agent_cli.core.state import Task, SystemState

class TestMessageSystem(unittest.TestCase):
    """Test cases for the message system"""
    
    def test_message_creation(self):
        """Test creating a message"""
        message = Message(
            sender_id="test_sender",
            receiver_id="test_receiver",
            message_type=MessageType.USER_REQUEST,
            payload={"test": "data"}
        )
        
        self.assertIsNotNone(message.id)
        self.assertEqual(message.sender_id, "test_sender")
        self.assertEqual(message.receiver_id, "test_receiver")
        self.assertEqual(message.message_type, MessageType.USER_REQUEST)
        self.assertEqual(message.payload, {"test": "data"})
        self.assertIsInstance(message.timestamp, datetime)
    
    def test_message_type_constants(self):
        """Test message type constants"""
        self.assertEqual(MessageType.USER_REQUEST, "user_request")
        self.assertEqual(MessageType.TASK_PLAN, "task_plan")
        self.assertEqual(MessageType.EXECUTION_RESULT, "execution_result")
        self.assertEqual(MessageType.VALIDATION_RESULT, "validation_result")
        self.assertEqual(MessageType.ERROR_REPORT, "error_report")
        self.assertEqual(MessageType.PROGRESS_UPDATE, "progress_update")

class TestStateSystem(unittest.TestCase):
    """Test cases for the state system"""
    
    def test_task_creation(self):
        """Test creating a task"""
        task = Task(
            task_id="test_task_1",
            name="Test Task",
            description="A test task",
            task_type="test",
            parameters={"param1": "value1"},
            dependencies=[],
            priority=1,
            status="pending"
        )
        
        self.assertEqual(task.task_id, "test_task_1")
        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.description, "A test task")
        self.assertEqual(task.task_type, "test")
        self.assertEqual(task.parameters, {"param1": "value1"})
        self.assertEqual(task.dependencies, [])
        self.assertEqual(task.priority, 1)
        self.assertEqual(task.status, "pending")
        self.assertIsNone(task.assigned_agent)
        self.assertIsInstance(task.created_at, datetime)
        self.assertIsInstance(task.updated_at, datetime)
    
    def test_system_state_creation(self):
        """Test creating a system state"""
        state = SystemState(
            session_id="test_session_1",
            timestamp=datetime.now(),
            user_id="test_user"
        )
        
        self.assertEqual(state.session_id, "test_session_1")
        self.assertEqual(state.user_id, "test_user")
        self.assertIsInstance(state.timestamp, datetime)
        self.assertIsNone(state.current_task)
        self.assertEqual(state.task_history, [])
        self.assertEqual(state.execution_context, {})
        self.assertEqual(state.active_agents, [])
        self.assertEqual(state.agent_states, {})
        self.assertEqual(state.message_queue, [])
        self.assertEqual(state.message_history, [])
        self.assertEqual(state.intermediate_results, {})
        self.assertEqual(state.final_results, [])
        self.assertEqual(state.errors, [])
        self.assertEqual(state.retry_count, 0)

if __name__ == '__main__':
    unittest.main()
