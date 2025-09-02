"""
Tool registry for managing and executing tools
"""
import asyncio
from typing import Dict, Any, Optional
from .base import Tool, ToolResult
from .weather_api import WeatherAPITool, WeatherConfig


class ToolRegistry:
    """Registry for managing and executing tools"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools"""
        # Register weather API tool
        weather_config = WeatherConfig()
        weather_tool = WeatherAPITool(weather_config)
        self.register_tool(weather_tool)
    
    def register_tool(self, tool: Tool):
        """Register a tool in the registry"""
        self.tools[tool.name()] = tool
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> list:
        """List all registered tools"""
        return list(self.tools.keys())
    
    async def execute_tool(self, name: str, **kwargs) -> ToolResult:
        """
        Execute a tool by name with provided arguments
        
        Args:
            name (str): Name of the tool to execute
            **kwargs: Arguments to pass to the tool
            
        Returns:
            ToolResult: Result of tool execution
        """
        tool = self.get_tool(name)
        if not tool:
            return ToolResult(
                tool_name=name,
                success=False,
                error=f"Tool '{name}' not found",
                data=None
            )
        
        try:
            return await tool.execute(**kwargs)
        except Exception as e:
            return ToolResult(
                tool_name=name,
                success=False,
                error=str(e),
                data=None
            )


# Global tool registry instance
tool_registry = ToolRegistry()
