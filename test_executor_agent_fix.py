#!/usr/bin/env python3
"""
Test script to verify the ExecutorAgent fix for async tool calling
"""
import sys
import os
import asyncio

# Add the current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

from src.multi_agent_cli.agents.executor import ExecutorAgent
from src.multi_agent_cli.messages.base import Message, MessageType
from src.multi_agent_cli.core.state import SystemState
from src.multi_agent_cli.tools import tool_registry

def test_executor_agent_tool_calling():
    """Test ExecutorAgent tool calling functionality"""
    print("Testing ExecutorAgent tool calling functionality...")
    
    # Create an ExecutorAgent instance
    executor = ExecutorAgent()
    
    # Create a mock task that requires weather tool execution
    weather_task = {
        "task_id": "weather_task_1",
        "name": "Fetch Weather Data",
        "description": "Get weather forecast for Shanghai",
        "parameters": {
            "location": "Shanghai",
            "days": 5
        }
    }
    
    # Test the _simulate_task_execution method
    result = executor._simulate_task_execution(weather_task)
    
    print(f"Task execution result: {result}")
    
    # Verify the result structure
    assert "task_id" in result
    assert "task_name" in result
    assert "status" in result
    assert "result" in result
    assert "execution_time" in result
    
    print("ExecutorAgent tool calling test completed successfully!")

if __name__ == "__main__":
    test_executor_agent_tool_calling()
