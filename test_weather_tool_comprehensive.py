#!/usr/bin/env python3
"""
Comprehensive test script to verify the weather tool functionality after fixing ToolResult initialization
"""

import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from src.multi_agent_cli.tools.registry import tool_registry
from src.multi_agent_cli.tools.weather_api import WeatherAPITool

async def test_weather_tool_comprehensive():
    """Comprehensive test of the weather tool after fixing ToolResult initialization"""
    print("=== Comprehensive Weather Tool Test ===")
    
    # Get the weather tool from registry
    weather_tool = tool_registry.get_tool("weather_api")
    if not weather_tool:
        print("ERROR: Weather tool not found in registry")
        return False
    
    print(f"Found weather tool: {weather_tool.name()}")
    print(f"Tool description: {weather_tool.description()}")
    print(f"Required parameters: {weather_tool.get_required_params()}")
    
    # Test 1: Tool registration
    print("\n--- Test 1: Tool Registration ---")
    available_tools = tool_registry.list_tools()
    print(f"Available tools: {available_tools}")
    if "weather_api" not in available_tools:
        print("ERROR: Weather API tool not properly registered")
        return False
    print("SUCCESS: Weather API tool is properly registered")
    
    # Test 2: Parameter validation
    print("\n--- Test 2: Parameter Validation ---")
    try:
        result = await weather_tool.execute()
        print(f"Result without location: {result}")
        if not result.success and "Location is required" in result.error:
            print("SUCCESS: Parameter validation works correctly")
        else:
            print("ERROR: Parameter validation failed")
            return False
    except Exception as e:
        print(f"EXCEPTION during parameter validation: {e}")
        return False
    
    # Test 3: API key validation
    print("\n--- Test 3: API Key Validation ---")
    try:
        result = await weather_tool.execute(location="Shanghai", days=5)
        print(f"Result with location but no API key: {result}")
        if not result.success and "Weather API key not configured" in result.error:
            print("SUCCESS: API key validation works correctly")
        else:
            print("ERROR: API key validation failed")
            return False
    except Exception as e:
        print(f"EXCEPTION during API key validation: {e}")
        return False
    
    # Test 4: Tool metadata
    print("\n--- Test 4: Tool Metadata ---")
    try:
        name = weather_tool.name()
        description = weather_tool.description()
        params = weather_tool.get_required_params()
        
        print(f"Tool name: {name}")
        print(f"Tool description: {description}")
        print(f"Required params: {params}")
        
        if name and description and isinstance(params, list):
            print("SUCCESS: Tool metadata is properly defined")
        else:
            print("ERROR: Tool metadata is incomplete")
            return False
    except Exception as e:
        print(f"EXCEPTION during metadata test: {e}")
        return False
    
    print("\n=== ALL TESTS PASSED ===")
    print("The ToolResult initialization fix is working correctly!")
    print("The weather tool is properly registered and validates inputs as expected.")
    return True

def main():
    """Main test function"""
    print("=== Weather Tool Comprehensive Test ===")
    
    try:
        # Run the async test
        result = asyncio.run(test_weather_tool_comprehensive())
        
        if result:
            print("\n=== COMPREHENSIVE TEST PASSED ===")
            return 0
        else:
            print("\n=== COMPREHENSIVE TEST FAILED ===")
            return 1
    except Exception as e:
        print(f"\n=== COMPREHENSIVE TEST FAILED WITH EXCEPTION ===")
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
