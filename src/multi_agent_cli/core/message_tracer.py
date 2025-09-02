from typing import Dict, List
import uuid
from datetime import datetime
from ..messages.base import Message


class MessageTracer:
    """Message tracer for tracking message flow"""
    
    def __init__(self):
        self.trace_storage: Dict[str, List[Dict]] = {}
    
    def create_trace_id(self) -> str:
        """Create a new trace ID"""
        return f"trace_{uuid.uuid4().hex[:8]}"
    
    def log_message_flow(self, trace_id: str, message: Message) -> None:
        """Log message flow with trace ID"""
        if trace_id not in self.trace_storage:
            self.trace_storage[trace_id] = []
        
        self.trace_storage[trace_id].append({
            'timestamp': datetime.now().isoformat(),
            'message_id': message.id,
            'sender': message.sender_id,
            'receiver': message.receiver_id,
            'type': message.message_type
        })
    
    def get_message_trace(self, trace_id: str) -> List[Dict]:
        """Get message trace by trace ID"""
        return self.trace_storage.get(trace_id, [])
