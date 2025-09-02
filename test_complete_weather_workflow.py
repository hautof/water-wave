"""
Complete test script for weather functionality in the multi-agent system
"""
import sys
import os
import asyncio

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath('.'))

from src.multi_agent_cli.workflow.workflow import MultiAgentWorkflow
from src.multi_agent_cli.messages.base import Message, MessageType

async def test_complete_weather_workflow():
    """Test the complete weather workflow in the multi-agent system"""
    print("Testing complete weather workflow in multi-agent system...")
    
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
        print(f"Final results count: {len(result.final_results)}")
        
        # Check if we have any final results
        if result.final_results:
            print("Final results:")
            for i, res in enumerate(result.final_results):
                print(f"  Result {i+1}: {res}")
        else:
            print("No final results found")
            
        # Check message history
        print(f"Message history length: {len(result.message_history)}")
        if result.message_history:
            print("Last 5 messages:")
            for msg in result.message_history[-5:]:
                print(f"  - {msg.message_type}: {msg.payload}")
                
        # Check if we have any intermediate results
        print(f"Intermediate results count: {len(result.intermediate_results)}")
        if result.intermediate_results:
            print("Intermediate results keys:")
            for key in result.intermediate_results.keys():
                print(f"  - {key}")
                
    except Exception as e:
        print(f"Error during workflow execution: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_complete_weather_workflow())
