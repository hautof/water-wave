"""
Weather API tool for fetching weather forecasts
"""
import os
import aiohttp
import asyncio
from typing import Dict, Any, Optional
from dataclasses import dataclass
from .base import Tool, ToolResult


@dataclass
class WeatherConfig:
    """Configuration for weather API"""
    api_key: Optional[str] = None
    base_url: str = "http://api.openweathermap.org/data/2.5"
    default_days: int = 7


class WeatherAPITool(Tool):
    """Tool for fetching weather data from OpenWeatherMap API"""
    
    def __init__(self, config: Optional[WeatherConfig] = None):
        self.config = config or WeatherConfig()
        # Try to get API key from environment if not provided
        if not self.config.api_key:
            self.config.api_key = os.getenv("OPENWEATHER_API_KEY")
    
    def name(self) -> str:
        return "weather_api"
    
    def description(self) -> str:
        return "Fetch weather forecast data for a specified location"
    
    def get_required_params(self) -> list:
        return ["location"]
    
    def get_optional_params(self) -> dict:
        return {
            "days": self.config.default_days
        }
    
    async def execute(self, **kwargs) -> ToolResult:
        """
        Execute the weather API tool to fetch forecast data
        
        Args:
            location (str): The location to fetch weather for
            days (int): Number of days to fetch (default: 7, max: 30)
        """
        location = kwargs.get("location")
        days = kwargs.get("days", self.config.default_days)
        
        # Validate inputs
        if not location:
            return ToolResult(
                tool_name=self.name(),
                success=False,
                error="Location is required",
                data=None
            )
        
        # Limit days to reasonable range
        days = min(max(days, 1), 30)
        
        # Check if we have an API key
        if not self.config.api_key:
            return ToolResult(
                tool_name=self.name(),
                success=False,
                error="Weather API key not configured",
                data=None
            )
        
        try:
            # Fetch weather data
            weather_data = await self._fetch_weather_data(location, days)
            return ToolResult(
                tool_name=self.name(),
                success=True,
                error=None,
                data=weather_data
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name(),
                success=False,
                error=str(e),
                data=None
            )
    
    async def _fetch_weather_data(self, location: str, days: int) -> Dict[str, Any]:
        """
        Fetch weather data from OpenWeatherMap API
        
        Args:
            location (str): Location name
            days (int): Number of days to fetch
            
        Returns:
            Dict containing weather forecast data
        """
        # For a forecast API, we would use:
        # /forecast/daily?q={location}&cnt={days}&appid={api_key}
        
        url = f"{self.config.base_url}/forecast"
        params = {
            "q": location,
            "appid": self.config.api_key,
            "cnt": days
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_weather_data(data, location, days)
                else:
                    raise Exception(f"API request failed with status {response.status}")
    
    def _process_weather_data(self, data: Dict[str, Any], location: str, days: int) -> Dict[str, Any]:
        """
        Process raw weather data into a more usable format
        
        Args:
            data (Dict): Raw API response
            location (str): Location name
            days (int): Number of days requested
            
        Returns:
            Dict containing processed weather data
        """
        processed_data = {
            "location": location,
            "requested_days": days,
            "forecasts": []
        }
        
        # Extract forecast data
        if "list" in data:
            for item in data["list"][:days]:
                forecast = {
                    "datetime": item.get("dt_txt", ""),
                    "temperature": {
                        "current": item.get("main", {}).get("temp"),
                        "min": item.get("main", {}).get("temp_min"),
                        "max": item.get("main", {}).get("temp_max")
                    },
                    "weather": item.get("weather", [{}])[0].get("description", ""),
                    "humidity": item.get("main", {}).get("humidity"),
                    "pressure": item.get("main", {}).get("pressure")
                }
                processed_data["forecasts"].append(forecast)
        
        return processed_data
