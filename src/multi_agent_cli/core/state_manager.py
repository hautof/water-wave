from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from langgraph.checkpoint import MemorySaver
from ..core.state import SystemState

class StateManager:
    """State manager integrating with LangGraph checkpointing"""
    
    def __init__(self):
        self.checkpointer = MemorySaver()
        self.states: Dict[str, SystemState] = {}
    
    async def save_checkpoint(self, session_id: str, state: SystemState):
        """Save a checkpoint of the system state"""
        self.states[session_id] = state
        # In a full implementation, this would use the LangGraph checkpointer
        # For now, we're just storing in memory
        pass
    
    async def load_checkpoint(self, session_id: str) -> Optional[SystemState]:
        """Load a checkpoint of the system state"""
        return self.states.get(session_id)
    
    async def update_state(self, session_id: str, updates: Dict[str, Any]):
        """Update the system state with new values"""
        if session_id in self.states:
            state = self.states[session_id]
            for key, value in updates.items():
                if hasattr(state, key):
                    setattr(state, key, value)
            # Update the timestamp
            state.timestamp = datetime.now()
        else:
            # Create a new state if it doesn't exist
            new_state = SystemState(
                session_id=session_id,
                timestamp=datetime.now(),
                user_id="default"
            )
            for key, value in updates.items():
                if hasattr(new_state, key):
                    setattr(new_state, key, value)
            self.states[session_id] = new_state
