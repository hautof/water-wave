import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class Message:
    """Base message class for inter-agent communication"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = ""
    receiver_id: str = ""
    message_type: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 0
    correlation_id: Optional[str] = None

class MessageType:
    """Message type constants"""
    USER_REQUEST = "user_request"
    TASK_PLAN = "task_plan"
    EXECUTION_RESULT = "execution_result"
    VALIDATION_RESULT = "validation_result"
    ERROR_REPORT = "error_report"
    PROGRESS_UPDATE = "progress_update"
    TASK_FEEDBACK = "task_feedback"
    EXECUTION_COMMAND = "execution_command"
    RETRY_REQUEST = "retry_request"
    VALIDATION_REQUEST = "validation_request"
    QUALITY_CHECK = "quality_check"
    QUALITY_REPORT = "quality_report"
