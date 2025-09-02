from typing import List, Dict, Any, Optional
import asyncio
import uuid
from ..messages.base import Message
from ..core.state import SystemState

class MessageBus:
    """Message bus for inter-agent communication"""
    
    def __init__(self):
        self.message_queue: List[Message] = []
        self.message_handlers: Dict[str, List] = {}
    
    async def send_message(self, message: Message) -> bool:
        """Send a message to the bus"""
        self.message_queue.append(message)
        # In a full implementation, this would notify the appropriate recipients
        return True
    
    async def broadcast_message(self, message: Message, recipients: List[str]) -> bool:
        """Broadcast a message to multiple recipients"""
        # In a full implementation, this would send the message to all specified recipients
        for recipient in recipients:
            message.receiver_id = recipient
            await self.send_message(message)
        return True
    
    def get_message_history(self, session_id: str) -> List[Message]:
        """Get message history for a session"""
        # In a full implementation, this would filter messages by session_id
        return self.message_queue[:]
    
    async def register_handler(self, message_type: str, handler):
        """Register a handler for a specific message type"""
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        self.message_handlers[message_type].append(handler)
    
    async def process_messages(self):
        """Process messages in the queue"""
        while self.message_queue:
            message = self.message_queue.pop(0)
            if message.message_type in self.message_handlers:
                for handler in self.message_handlers[message.message_type]:
                    await handler(message)
