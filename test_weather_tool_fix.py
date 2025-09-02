#!/usr/bin/env python3
"""
Test script to verify the weather tool functionality after fixing ToolResult initialization
"""

import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from src.multi_agent_cli.tools.registry import tool_registry
from src.multi_agent_cli.tools.weather_api import WeatherAPITool

async def test_weather_tool_fix():
    """Test the weather tool after fixing ToolResult initialization"""
    print("Testing weather tool functionality after ToolResult fix...")
    
    # Get the weather tool from registry
    weather_tool = tool_registry.get_tool("weather_api")
    if not weather_tool:
        print("ERROR: Weather tool not found in registry")
        return False
    
    print(f"Found weather tool: {weather_tool.name()}")
    print(f"Tool description: {weather_tool.description()}")
    print(f"Required parameters: {weather_tool.get_required_params()}")
    
    # Test the tool with required parameters (Shanghai, 5 days)
    print("\nTesting tool execution with required parameters...")
    try:
        result = await weather_tool.execute(location="Shanghai", days=5)
        print(f"Tool execution result: {result}")
        
        if result.success:
            print("SUCCESS: Weather tool executed successfully")
            print(f"Data: {result.data}")
            return True
        else:
            print(f"ERROR: Tool execution failed: {result.error}")
            return False
    except Exception as e:
        print(f"EXCEPTION: Error during tool execution: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("=== Weather Tool Fix Verification ===")
    
    try:
        # Run the async test
        result = asyncio.run(test_weather_tool_fix())
        
        if result:
            print("\n=== TEST PASSED ===")
            return 0
        else:
            print("\n=== TEST FAILED ===")
            return 1
    except Exception as e:
        print(f"\n=== TEST FAILED WITH EXCEPTION ===")
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
