"""
Unit tests for the Weather Server MCP server.

Tests cover weather API integration and error handling with mocked API responses.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from weather import get_weather


class TestWeatherAPIIntegration:
    """Test cases for the get_weather() function with OpenWeatherMap API."""
    
    @pytest.mark.asyncio
    async def test_get_weather_successful_response(self):
        """Test successful weather API call."""
        mock_response = {
            "name": "New York",
            "sys": {"country": "US"},
            "weather": [{"description": "Clear sky"}],
            "main": {"temp": 20.5, "feels_like": 19.2, "humidity": 65},
            "wind": {"speed": 5.2}
        }
        
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            result = await get_weather("New York")
            
            assert isinstance(result, str)
            assert "New York" in result
            assert "Clear sky" in result
            assert "20.5" in result
            assert "65" in result
            mock_get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_weather_with_country_code(self):
        """Test weather response includes country code."""
        mock_response = {
            "name": "London",
            "sys": {"country": "GB"},
            "weather": [{"description": "Rainy"}],
            "main": {"temp": 15.0, "feels_like": 13.5, "humidity": 80},
            "wind": {"speed": 3.1}
        }
        
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            result = await get_weather("London")
            
            assert "London, GB" in result or "London" in result
            assert "Rainy" in result
    
    @pytest.mark.asyncio
    async def test_get_weather_temperature_formatting(self):
        """Test that temperature is properly formatted in response."""
        mock_response = {
            "name": "Tokyo",
            "sys": {"country": "JP"},
            "weather": [{"description": "Partly cloudy"}],
            "main": {"temp": 25.8, "feels_like": 24.3, "humidity": 72},
            "wind": {"speed": 4.5}
        }
        
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            result = await get_weather("Tokyo")
            
            assert "25.8°C" in result
            assert "feels like 24.3°C" in result or "24.3°C" in result


class TestWeatherErrorHandling:
    """Test cases for error handling in weather server."""
    
    @pytest.mark.asyncio
    async def test_empty_location_raises_error(self):
        """Test that empty location raises ValueError."""
        with pytest.raises(ValueError, match="Location cannot be empty"):
            await get_weather("")
    
    @pytest.mark.asyncio
    async def test_whitespace_only_location_raises_error(self):
        """Test that whitespace-only location raises ValueError."""
        with pytest.raises(ValueError, match="Location cannot be empty"):
            await get_weather("   ")
    
    @pytest.mark.asyncio
    async def test_non_string_location_raises_error(self):
        """Test that non-string location raises ValueError."""
        with pytest.raises(ValueError, match="Invalid location"):
            await get_weather(None)
        
        with pytest.raises(ValueError, match="Invalid location"):
            await get_weather(123)
        
        with pytest.raises(ValueError, match="Invalid location"):
            await get_weather([])
    
    @pytest.mark.asyncio
    async def test_invalid_api_key_error(self):
        """Test error handling for invalid API key."""
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 401
            
            with pytest.raises(ValueError, match="Invalid OpenWeatherMap API key"):
                await get_weather("London")
    
    @pytest.mark.asyncio
    async def test_location_not_found_error(self):
        """Test error handling for non-existent location."""
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 404
            
            with pytest.raises(ValueError, match="not found"):
                await get_weather("FakeCity123")
    
    @pytest.mark.asyncio
    async def test_api_service_error(self):
        """Test error handling for API service errors."""
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 500
            
            with pytest.raises(ValueError, match="Weather service error"):
                await get_weather("Paris")
    
    @pytest.mark.asyncio
    async def test_request_timeout_error(self):
        """Test error handling for request timeout."""
        import requests
        
        with patch("requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout()
            
            with pytest.raises(ValueError, match="timed out"):
                await get_weather("Berlin")
    
    @pytest.mark.asyncio
    async def test_connection_error(self):
        """Test error handling for connection errors."""
        import requests
        
        with patch("requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError()
            
            with pytest.raises(ValueError, match="Unable to connect"):
                await get_weather("Sydney")
    
    @pytest.mark.asyncio
    async def test_unexpected_response_format(self):
        """Test error handling for unexpected API response."""
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"invalid": "response"}
            
            with pytest.raises(ValueError, match="unexpected data format"):
                await get_weather("Rome")


class TestWeatherInputHandling:
    """Test cases for input handling and normalization."""
    
    @pytest.mark.asyncio
    async def test_location_whitespace_stripping(self):
        """Test that location whitespace is properly stripped."""
        mock_response = {
            "name": "Paris",
            "sys": {"country": "FR"},
            "weather": [{"description": "Sunny"}],
            "main": {"temp": 22.0, "feels_like": 21.0, "humidity": 50},
            "wind": {"speed": 2.5}
        }
        
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            # Test with leading/trailing whitespace
            result = await get_weather("  Paris  ")
            
            assert isinstance(result, str)
            assert len(result) > 0
            # Check that the request was made with stripped location
            call_args = mock_get.call_args
            assert "Paris" in str(call_args)


class TestWeatherResponseFormat:
    """Test cases for response format consistency."""
    
    @pytest.mark.asyncio
    async def test_response_contains_all_weather_info(self):
        """Test that response contains all expected weather information."""
        mock_response = {
            "name": "Barcelona",
            "sys": {"country": "ES"},
            "weather": [{"description": "Partly cloudy"}],
            "main": {"temp": 18.5, "feels_like": 17.2, "humidity": 70},
            "wind": {"speed": 6.3}
        }
        
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            result = await get_weather("Barcelona")
            result_lower = result.lower()
            
            # Check for key information
            assert "barcelona" in result_lower or "Weather" in result
            assert "condition:" in result_lower or "partly cloudy" in result_lower
            assert "temperature:" in result_lower or "18.5" in result
            assert "humidity:" in result_lower or "70" in result
            assert "wind" in result_lower
    
    @pytest.mark.asyncio
    async def test_response_string_type(self):
        """Test that response is always a string."""
        mock_response = {
            "name": "Amsterdam",
            "sys": {"country": "NL"},
            "weather": [{"description": "Rainy"}],
            "main": {"temp": 12.0, "feels_like": 11.0, "humidity": 85},
            "wind": {"speed": 7.2}
        }
        
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            result = await get_weather("Amsterdam")
            
            assert isinstance(result, str)
            assert len(result) > 0


class TestWeatherAsyncExecution:
    """Test cases for async execution behavior."""
    
    @pytest.mark.asyncio
    async def test_concurrent_weather_queries(self):
        """Test that multiple concurrent queries can be executed."""
        mock_response = {
            "name": "City",
            "sys": {"country": "XX"},
            "weather": [{"description": "Clear"}],
            "main": {"temp": 20.0, "feels_like": 19.0, "humidity": 60},
            "wind": {"speed": 3.0}
        }
        
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            results = await asyncio.gather(
                get_weather("City1"),
                get_weather("City2"),
                get_weather("City3")
            )
            
            assert len(results) == 3
            assert all(isinstance(r, str) for r in results)
            assert all(len(r) > 0 for r in results)
    
    @pytest.mark.asyncio
    async def test_rapid_sequential_queries(self):
        """Test rapid sequential queries work correctly."""
        mock_response = {
            "name": "City",
            "sys": {"country": "XX"},
            "weather": [{"description": "Cloudy"}],
            "main": {"temp": 15.0, "feels_like": 14.0, "humidity": 75},
            "wind": {"speed": 4.0}
        }
        
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            locations = ["City1", "City2", "City3", "City4", "City5"]
            results = []
            
            for location in locations:
                result = await get_weather(location)
                results.append(result)
            
            assert len(results) == len(locations)
            assert all(isinstance(r, str) for r in results)


def run_async_test(coro):
    """Helper function to run async tests."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
