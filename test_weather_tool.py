"""
Test script for weather tool functionality
"""
import sys
import os
import asyncio

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath('.'))

from src.multi_agent_cli.tools.base import tool_registry, ToolResult

async def test_weather_tool():
    """Test the weather API tool"""
    print("Testing weather tool...")
    
    # Try to get the weather tool
    weather_tool = tool_registry.get_tool("weather_api")
    if not weather_tool:
        print("ERROR: Weather tool not found in registry")
        return
    
    print(f"Found weather tool: {weather_tool.name}")
    print(f"Tool description: {weather_tool.description}")
    
    # Try to execute the tool (this will likely fail without an API key)
    print("\nTesting tool execution...")
    try:
        result = await weather_tool.execute(location="Shanghai", days=3)
        print(f"Execution result: {result}")
        if result.success:
            print(f"Success! Weather data: {result.data}")
        else:
            print(f"Expected failure: {result.error}")
    except Exception as e:
        print(f"Exception during execution: {e}")
    
    print("\nWeather tool test completed.")

if __name__ == "__main__":
    asyncio.run(test_weather_tool())
