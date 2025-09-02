from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
from ..messages.base import Message

@dataclass
class Task:
    """Task definition"""
    task_id: str
    name: str
    description: str
    task_type: str
    parameters: Dict[str, Any]
    dependencies: List[str]
    priority: int
    status: str
    assigned_agent: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class SystemState:
    """Global system state"""
    # Session information
    session_id: str = field(default_factory=lambda: f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    timestamp: datetime = field(default_factory=datetime.now)
    user_id: str = "default_user"
    
    # Task state
    current_task: Optional[Task] = None
    task_history: List[Task] = field(default_factory=list)
    execution_context: Dict[str, Any] = field(default_factory=dict)
    
    # Agent state
    active_agents: List[str] = field(default_factory=list)
    agent_states: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Message queue
    message_queue: List[Message] = field(default_factory=list)
    message_history: List[Message] = field(default_factory=list)
    
    # Result storage
    intermediate_results: Dict[str, Any] = field(default_factory=dict)
    final_results: List[Any] = field(default_factory=list)
    
    # Error handling
    errors: List[Dict[str, Any]] = field(default_factory=list)
    retry_count: int = 0
    
    # Current message for workflow processing
    current_message: Optional[Message] = None
    messages: List[Message] = field(default_factory=list)
