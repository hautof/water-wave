import pytest
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.multi_agent_cli.agents.analyst import AnalystAgent
from src.multi_agent_cli.agents.executor import ExecutorAgent
from src.multi_agent_cli.agents.validator import ValidatorAgent
from src.multi_agent_cli.messages.base import Message, MessageType
from src.multi_agent_cli.core.state import SystemState

def test_analyst_agent_creation():
    """Test that analyst agent can be created with correct attributes"""
    agent = AnalystAgent()
    
    assert agent.agent_id == "analyst"
    assert agent.name == "Analyst Agent"
    assert "requirement_analysis" in agent.get_capabilities()
    assert "task_decomposition" in agent.get_capabilities()
    assert "strategy_planning" in agent.get_capabilities()

def test_executor_agent_creation():
    """Test that executor agent can be created with correct attributes"""
    agent = ExecutorAgent()
    
    assert agent.agent_id == "executor"
    assert agent.name == "Executor Agent"
    assert "command_execution" in agent.get_capabilities()
    assert "file_operations" in agent.get_capabilities()
    assert "api_calls" in agent.get_capabilities()

def test_validator_agent_creation():
    """Test that validator agent can be created with correct attributes"""
    agent = ValidatorAgent()
    
    assert agent.agent_id == "validator"
    assert agent.name == "Validator Agent"
    assert "result_validation" in agent.get_capabilities()
    assert "quality_assurance" in agent.get_capabilities()
    assert "compliance_check" in agent.get_capabilities()

def test_analyst_message_validation():
    """Test that analyst agent can validate messages correctly"""
    agent = AnalystAgent()
    
    # Valid message types for analyst
    valid_message = Message(
        sender_id="user",
        receiver_id="analyst",
        message_type=MessageType.USER_REQUEST,
        payload={"text": "Test request"}
    )
    
    assert agent.validate_input(valid_message) == True

def test_state_creation():
    """Test that SystemState can be created with default values"""
    state = SystemState(session_id="test_session", user_id="test_user")
    
    assert state.session_id == "test_session"
    assert state.user_id == "test_user"
    assert state.retry_count == 0
    assert state.task_history == []
    assert state.message_history == []
