from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .state import SystemState
from ..messages.base import Message

class Agent(ABC):
    """Base agent interface"""
    
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.state = {}
    
    @abstractmethod
    async def process_message(self, message: Message, state: SystemState) -> List[Message]:
        """Process received message"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        pass
    
    @abstractmethod
    def validate_input(self, message: Message) -> bool:
        """Validate input message format"""
        pass
