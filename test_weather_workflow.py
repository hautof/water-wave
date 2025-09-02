"""
Test script for weather workflow functionality
"""
import sys
import os
import asyncio

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath('.'))

from src.multi_agent_cli.workflow.workflow import MultiAgentWorkflow
from src.multi_agent_cli.messages.base import Message, MessageType

async def test_weather_workflow():
    """Test the full workflow with a weather-related request"""
    print("Testing weather workflow...")
    
    # Create workflow instance
    workflow = MultiAgentWorkflow()
    
    # Create a proper test message with the correct payload structure
    test_message = Message(
        id='weather_test_1',
        sender_id='user',
        receiver_id='analyst',
        message_type=MessageType.USER_REQUEST,
        payload={'text': 'Get the weather forecast for Shanghai for the next 30 days'},
    )
    
    # Test running the workflow with a weather-related request
    session_id = "weather_test_session"
    
    try:
        result = await workflow.run(test_message, session_id)
        print("Workflow execution completed successfully")
        print(f"Result type: {type(result)}")
        if hasattr(result, '__dict__'):
            print(f"Result attributes: {result.__dict__.keys()}")
    except Exception as e:
        print(f"Error during workflow execution: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_weather_workflow())
