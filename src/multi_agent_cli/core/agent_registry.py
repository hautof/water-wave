from typing import Dict, List, Optional
from .agent import Agent

class AgentRegistry:
    """Agent registry for dynamic agent management"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.agent_configs: Dict[str, Dict] = {}
    
    def register_agent(self, agent: Agent, config: Dict = None):
        """Register an agent with optional configuration"""
        self.agents[agent.agent_id] = agent
        if config:
            self.agent_configs[agent.agent_id] = config
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent by ID"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            if agent_id in self.agent_configs:
                del self.agent_configs[agent_id]
            return True
        return False
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get an agent instance by ID"""
        return self.agents.get(agent_id)
    
    def list_available_agents(self) -> List[str]:
        """List all available agent IDs"""
        return list(self.agents.keys())
    
    def get_agent_config(self, agent_id: str) -> Optional[Dict]:
        """Get configuration for an agent by ID"""
        return self.agent_configs.get(agent_id)