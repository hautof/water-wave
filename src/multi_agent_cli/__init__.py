"""Multi-Agent CLI Tool based on LangGraph framework"""

__version__ = "0.1.0"

# Import core components
from .core.agent import Agent
from .core.agent_registry import AgentRegistry
from .messages.base import Message, MessageType
from .core.state import SystemState, Task

# Import agents
from .agents.analyst import AnalystAgent
from .agents.executor import ExecutorAgent
from .agents.validator import ValidatorAgent

__all__ = [
    "Agent",
    "AgentRegistry",
    "Message",
    "MessageType",
    "SystemState",
    "Task",
    "AnalystAgent",
    "ExecutorAgent",
    "ValidatorAgent"
]