"""
WeatherServer - A Model Context Protocol (MCP) server providing real weather information.

This module provides weather tools that call OpenWeatherMap API to get current weather
conditions for any location. Requires OPENWEATHER_API_KEY in environment variables.
"""

import os
import logging
import requests
from mcp.server.fastmcp import FastMCP
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging for debugging and monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the FastMCP server with a descriptive name
mcp = FastMCP("Weather")

# Get API key from environment (after loading .env)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@mcp.tool()
async def get_weather(location: str) -> str:
    """
    Get the current weather for a given location using OpenWeatherMap API.
    
    Args:
        location (str): The location to get weather for (city name, e.g., "California", "New York")
    
    Returns:
        str: A formatted string describing the current weather conditions including:
             - Temperature (in Celsius)
             - Weather description
             - Humidity
             - Wind speed
    
    Raises:
        ValueError: If location is empty, invalid, or API key is not configured
        Exception: If weather service is unavailable or API request fails
    
    Note:
        Requires OPENWEATHER_API_KEY environment variable to be set.
        Get a free API key from: https://openweathermap.org/api
    """
    try:
        # Validate API key configuration
        if not OPENWEATHER_API_KEY:
            raise ValueError(
                "OPENWEATHER_API_KEY is not configured. "
                "Get a free key from https://openweathermap.org/api and add it to .env"
            )
        
        # Validate input
        if not location or not isinstance(location, str):
            raise ValueError(f"Invalid location: expected non-empty string, got {type(location).__name__}")
        
        # Strip whitespace and validate
        location = location.strip()
        if not location:
            raise ValueError("Location cannot be empty")
        
        logger.info(f"Fetching weather for location: {location}")
        
        # Make API request to OpenWeatherMap
        params = {
            "q": location,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"  # Use Celsius
        }
        
        response = requests.get(OPENWEATHER_BASE_URL, params=params, timeout=10)
        
        # Check if request was successful
        if response.status_code == 401:
            raise ValueError("Invalid OpenWeatherMap API key. Check your OPENWEATHER_API_KEY in .env")
        elif response.status_code == 404:
            raise ValueError(f"Location '{location}' not found. Please check the spelling and try again.")
        elif response.status_code != 200:
            raise ValueError(f"Weather service error (Status {response.status_code}). Please try again later.")
        
        # Parse response
        data = response.json()
        
        # Extract weather information
        weather_description = data["weather"][0]["description"].capitalize()
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        city_name = data["name"]
        country = data["sys"].get("country", "")
        
        # Format response
        location_str = f"{city_name}, {country}" if country else city_name
        weather_response = (
            f"Weather in {location_str}:\n"
            f"  Condition: {weather_description}\n"
            f"  Temperature: {temperature}°C (feels like {feels_like}°C)\n"
            f"  Humidity: {humidity}%\n"
            f"  Wind Speed: {wind_speed} m/s"
        )
        
        logger.info(f"Successfully fetched weather for {location}: {weather_description}")
        return weather_response
        
    except ValueError as e:
        logger.error(f"Validation error for location '{location}': {str(e)}")
        raise
    except requests.exceptions.Timeout:
        logger.error(f"Request timeout while fetching weather for '{location}'")
        raise ValueError("Weather service request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error while fetching weather for '{location}'")
        raise ValueError("Unable to connect to weather service. Check your internet connection.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error while fetching weather for '{location}': {str(e)}")
        raise ValueError(f"Weather service error: {str(e)}")
    except KeyError as e:
        logger.error(f"Unexpected API response format: {str(e)}")
        raise ValueError("Weather service returned unexpected data format. Please try again.")
    except Exception as e:
        logger.error(f"Unexpected error fetching weather for '{location}': {str(e)}")
        raise ValueError(f"Failed to fetch weather data: {str(e)}")


if __name__ == "__main__":
    logger.info("Starting WeatherServer on stdio transport...")
    try:
        # Warn if API key is not configured
        if not OPENWEATHER_API_KEY:
            logger.warning(
                "OPENWEATHER_API_KEY is not configured. "
                "Get a free API key from https://openweathermap.org/api and add it to .env"
            )
        
        mcp.run(transport="stdio")
    except Exception as e:
        logger.error(f"Error starting WeatherServer: {str(e)}")
        raise
