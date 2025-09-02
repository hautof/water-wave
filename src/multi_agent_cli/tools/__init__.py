"""
Tools package for the multi-agent CLI tool
"""
from .registry import tool_registry
from .base import Tool, ToolResult
from .weather_api import WeatherAPITool, WeatherConfig

__all__ = ['tool_registry', 'Tool', 'ToolResult', 'WeatherAPITool', 'WeatherConfig']
