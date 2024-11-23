import asyncio
import unittest
from unittest.mock import patch, AsyncMock

import httpx

from services.weather import *
from settings import settings
from models import WeatherQuery


class TestWeatherService(unittest.IsolatedAsyncioTestCase):
    @patch("httpx.AsyncClient.get", new_callable=AsyncMock)
    async def test_fetch_weather_success(self, mock_get):
        # Prepare data
        data = WeatherQuery(lat=34.0522, lon=-118.2437, units="metric")
        mock_response = {
            "weather": [{
                "description": "clear sky"
            }],
            "main": {
                "temp": 27.5
            }
        }

        # Define mock behavior
        mock_get.return_value.__aenter__.return_value.json.return_value = mock_response

        # Call the function
        response = asyncio.run(fetch_weather(data))

        # Assert function behavior
        self.assertEqual(response.weather[0].description, "clear sky")
        self.assertEqual(response.main.temp, 27.5)
        mock_get.assert_awaited_once_with(
            f"{settings.OPEN_WEATHER_API_URL}weather?lat={data.lat}&lon={data.lon}&units={data.units}&appid={settings.API_KEY}"
        )

    @patch("httpx.AsyncClient.get", new_callable=AsyncMock)
    async def test_fetch_weather_failure(self, mock_get):
        # Prepare data
        data = WeatherQuery(lat=-999, lon=-999, units="metric")  # Invalid coordinates

        # Define mock behavior
        mock_get.return_value.__aenter__.return_value.raise_for_status.side_effect = httpx.HTTPStatusError

        # Call the function and assert exception
        with self.assertRaises(httpx.HTTPStatusError):
            await fetch_weather(data)

    @patch("httpx.AsyncClient", new_callable=AsyncMock)
    async def test_fetch_forecast(self, mock_client):
        # Construct a mock return value
        mock_response = AsyncMock(httpx.Response)
        mock_response.json.return_value = {"forecast": "sunny"}
        # Set the async context manager return value
        mock_client.return_value.__aenter__.return_value = mock_response

        # Create a sample WeatherQuery
        query = WeatherQuery(lat=12.34, lon=56.78, units="metric", cnt=7)

        result = await fetch_forecast(query)
        self.assertEqual(result, {"forecast": "sunny"})

    @patch("httpx.AsyncClient", new_callable=AsyncMock)
    async def test_fetch_forecast_failure(self, mock_client):
        # Prepare data
        data = WeatherQuery(lat=-999, lon=-999, units="metric")  # Invalid coordinates

        # Define mock behavior
        mock_client.return_value.__aenter__.return_value.raise_for_status.side_effect = httpx.HTTPStatusError

        # Call the function and assert exception
        with self.assertRaises(httpx.HTTPStatusError):
            await fetch_forecast(data)


if __name__ == "__main__":
    unittest.main()
