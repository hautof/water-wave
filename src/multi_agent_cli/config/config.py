import yaml
import os
from typing import Dict, Any
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AgentConfig:
    """Agent configuration settings"""
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1500
    capabilities: list = field(default_factory=list)


@dataclass
class SystemConfig:
    """System-wide configuration settings"""
    max_retry_attempts: int = 3
    timeout_seconds: int = 300
    log_level: str = "INFO"


@dataclass
class MessageBusConfig:
    """Message bus configuration settings"""
    queue_size: int = 1000
    batch_size: int = 10
    retry_delay: int = 5


@dataclass
class Config:
    """Main configuration class"""
    system: SystemConfig = field(default_factory=SystemConfig)
    agents: Dict[str, AgentConfig] = field(default_factory=dict)
    message_bus: MessageBusConfig = field(default_factory=MessageBusConfig)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'Config':
        """Create Config instance from dictionary"""
        system = SystemConfig(**config_dict.get('system', {}))
        
        agents = {}
        for agent_name, agent_config in config_dict.get('agents', {}).items():
            agents[agent_name] = AgentConfig(**agent_config)
            
        message_bus = MessageBusConfig(**config_dict.get('message_bus', {}))
        
        return cls(system=system, agents=agents, message_bus=message_bus)


def load_config(config_path: str = None) -> Config:
    """Load configuration from YAML file"""
    if config_path is None:
        # Try to find config in common locations
        possible_paths = [
            "./config.yaml",
            "./config.yml",
            "~/.multi-agent-cli/config.yaml",
            "~/.multi-agent-cli/config.yml",
            "/etc/multi-agent-cli/config.yaml"
        ]
        
        for path in possible_paths:
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                config_path = expanded_path
                break
        else:
            # Return default configuration if no config file found
            return Config()
    
    try:
        with open(config_path, 'r') as file:
            config_dict = yaml.safe_load(file)
        return Config.from_dict(config_dict)
    except FileNotFoundError:
        print(f"Configuration file {config_path} not found. Using default configuration.")
        return Config()
    except yaml.YAMLError as e:
        print(f"Error parsing YAML configuration file: {e}. Using default configuration.")
        return Config()


def create_default_config_file(config_path: str = "./config.yaml") -> None:
    """Create a default configuration file"""
    default_config = {
        "system": {
            "max_retry_attempts": 3,
            "timeout_seconds": 300,
            "log_level": "INFO"
        },
        "agents": {
            "analyst": {
                "model": "gpt-4",
                "temperature": 0.2,
                "max_tokens": 2000,
                "capabilities": [
                    "requirement_analysis",
                    "task_decomposition",
                    "strategy_planning"
                ]
            },
            "executor": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.1,
                "max_tokens": 1500,
                "capabilities": [
                    "command_execution",
                    "file_operations",
                    "api_calls"
                ]
            },
            "validator": {
                "model": "gpt-4",
                "temperature": 0.0,
                "max_tokens": 1000,
                "capabilities": [
                    "result_validation",
                    "quality_assurance",
                    "compliance_check"
                ]
            }
        },
        "message_bus": {
            "queue_size": 1000,
            "batch_size": 10,
            "retry_delay": 5
        }
    }
    
    # Create directory if it doesn't exist
    Path(config_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as file:
        yaml.dump(default_config, file, default_flow_style=False, sort_keys=False)
    
    print(f"Default configuration file created at {config_path}")
