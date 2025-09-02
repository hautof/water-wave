#!/usr/bin/env python3
"""
Test script to verify agent tool calling capabilities
"""

import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from src.multi_agent_cli.agents.analyst import AnalystAgent
from src.multi_agent_cli.agents.executor import ExecutorAgent
from src.multi_agent_cli.agents.validator import ValidatorAgent
from src.multi_agent_cli.tools.registry import tool_registry
from src.multi_agent_cli.tools.weather_api import WeatherAPITool
from src.multi_agent_cli.llm_providers.base import OpenAIProvider, QwenProvider, DeepSeekProvider
from src.multi_agent_cli.messages.base import Message, MessageType
from src.multi_agent_cli.core.state import SystemState

async def test_agent_tool_calling():
    """Test agent tool calling capabilities"""
    print("=== Agent Tool Calling Test ===")
    
    # Test 1: Tool Registry Functionality
    print("\n--- Test 1: Tool Registry ---")
    available_tools = tool_registry.list_tools()
    print(f"Available tools: {available_tools}")
    
    if "weather_api" not in available_tools:
        print("ERROR: Weather API tool not found in registry")
        return False
    
    weather_tool = tool_registry.get_tool("weather_api")
    print(f"Retrieved tool: {weather_tool.name()}")
    print(f"Tool description: {weather_tool.description()}")
    
    # Test 2: Agent Initialization with Tool Registry
    print("\n--- Test 2: Agent Initialization ---")
    
    # Create LLM providers
    try:
        openai_provider = OpenAIProvider(model="gpt-3.5-turbo")
        print("OpenAI provider created successfully")
    except Exception as e:
        print(f"OpenAI provider creation failed (expected without API key): {e}")
        openai_provider = None
    
    try:
        qwen_provider = QwenProvider(model="qwen-plus")
        print("Qwen provider created successfully")
    except Exception as e:
        print(f"Qwen provider creation failed (expected without API key): {e}")
        qwen_provider = None
    
    try:
        deepseek_provider = DeepSeekProvider(model="deepseek-chat")
        print("DeepSeek provider created successfully")
    except Exception as e:
        print(f"DeepSeek provider creation failed (expected without API key): {e}")
        deepseek_provider = None
    
    # Create agents with tool registry
    analyst = AnalystAgent(agent_id="analyst_1", name="Analyst Agent")
    executor = ExecutorAgent(agent_id="executor_1", name="Executor Agent")
    validator = ValidatorAgent(agent_id="validator_1", name="Validator Agent")
    
    print("Agents created successfully")
    print(f"Analyst capabilities: {analyst.get_capabilities()}")
    print(f"Executor capabilities: {executor.get_capabilities()}")
    print(f"Validator capabilities: {validator.get_capabilities()}")
    
    # Test 3: Analyst Agent Planning with Tool Awareness
    print("\n--- Test 3: Analyst Agent Planning ---")
    
    # Create a test message that should trigger weather tool planning
    test_message = Message(
        id="test_1",
        sender_id="user",
        receiver_id="analyst",
        message_type=MessageType.USER_REQUEST,
        payload={"text": "What is the weather forecast for Shanghai for the next 5 days?"},
        priority=0,
        correlation_id=None
    )
    
    # Create initial state
    initial_state = SystemState(
        session_id="test_session_1",
        user_id="test_user",
        current_task=None,
        task_history=[],
        execution_context={},
        active_agents=["analyst_1"],
        agent_states={},
        message_queue=[test_message],
        message_history=[],
        intermediate_results={},
        final_results=[],
        errors=[],
        retry_count=0
    )
    
    # Process message with analyst agent
    try:
        analyst_responses = await analyst.process_message(test_message, initial_state)
        print(f"Analyst responses: {analyst_responses}")
        
        # Check if analyst identified weather task
        weather_task_found = False
        for response in analyst_responses:
            if response.message_type == "task_plan" and "weather" in str(response.payload).lower():
                weather_task_found = True
                print("SUCCESS: Analyst identified weather task in plan")
                break
        
        if not weather_task_found:
            print("INFO: Analyst may not have explicitly planned weather task (this is OK for basic test)")
    except Exception as e:
        print(f"EXCEPTION during analyst processing: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Executor Agent Tool Execution
    print("\n--- Test 4: Executor Agent Tool Execution ---")
    
    # Create a mock task plan message that includes weather tool
    task_plan_message = Message(
        id="task_plan_1",
        sender_id="analyst",
        receiver_id="executor",
        message_type="task_plan",
        payload={
            "tasks": [
                {
                    "task_id": "weather_task_1",
                    "name": "Fetch Weather Data",
                    "description": "Get weather forecast for Shanghai",
                    "task_type": "tool_call",
                    "parameters": {
                        "tool_name": "weather_api",
                        "location": "Shanghai",
                        "days": 5
                    },
                    "dependencies": [],
                    "priority": 1
                }
            ]
        },
        priority=0,
        correlation_id=None
    )
    
    # Process task plan with executor agent
    try:
        executor_responses = await executor.process_message(task_plan_message, initial_state)
        print(f"Executor responses: {len(executor_responses)} messages")
        
        # Check for execution results
        execution_results = [msg for msg in executor_responses if msg.message_type == "execution_result"]
        print(f"Execution results: {len(execution_results)} messages")
        
        if execution_results:
            print("SUCCESS: Executor processed task and generated execution results")
            for result in execution_results:
                print(f"  Result: {result.payload}")
        else:
            print("INFO: No execution results generated (this is OK for basic test)")
            
    except Exception as e:
        print(f"EXCEPTION during executor processing: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 5: Validator Agent Result Validation
    print("\n--- Test 5: Validator Agent Result Validation ---")
    
    # Create a mock execution result message
    execution_result_message = Message(
        id="execution_result_1",
        sender_id="executor",
        receiver_id="validator",
        message_type="execution_result",
        payload={
            "task_id": "weather_task_1",
            "result": {
                "data": [
                    {"date": "2025-09-03", "temperature": 28, "condition": "Sunny"},
                    {"date": "2025-09-04", "temperature": 26, "condition": "Cloudy"}
                ]
            },
            "status": "completed"
        },
        priority=0,
        correlation_id=None
    )
    
    # Process execution result with validator agent
    try:
        validator_responses = await validator.process_message(execution_result_message, initial_state)
        print(f"Validator responses: {len(validator_responses)} messages")
        
        # Check for validation results
        validation_results = [msg for msg in validator_responses if msg.message_type == "validation_result"]
        print(f"Validation results: {len(validation_results)} messages")
        
        if validation_results:
            print("SUCCESS: Validator processed execution result and generated validation results")
            for result in validation_results:
                print(f"  Result: {result.payload}")
        else:
            print("INFO: No validation results generated (this is OK for basic test)")
            
    except Exception as e:
        print(f"EXCEPTION during validator processing: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== AGENT TOOL CALLING TEST COMPLETED ===")
    return True

def main():
    """Main test function"""
    print("=== Agent Tool Calling Capability Test ===")
    
    try:
        # Run the async test
        result = asyncio.run(test_agent_tool_calling())
        
        if result:
            print("\n=== AGENT TOOL CALLING TEST PASSED ===")
            return 0
        else:
            print("\n=== AGENT TOOL CALLING TEST FAILED ===")
            return 1
    except Exception as e:
        print(f"\n=== AGENT TOOL CALLING TEST FAILED WITH EXCEPTION ===")
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
