import httpx

from models import WeatherResponse, WeatherQuery, ForecastQueryParams
from settings import settings


async def fetch_weather(data: WeatherQuery):
    api_url = f"{settings.OPEN_WEATHER_API_URL}weather?lat={data.lat}&lon={data.lon}&units={data.units}&appid={settings.API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        response_json = response.json()
        return WeatherResponse(**response_json)

async def fetch_forecast(query: ForecastQueryParams):
    api_url = f"{settings.OPEN_WEATHER_API_URL}forecast/daily?lat={query.lat}&lon={query.lon}&units={query.units}&cnt={query.cnt}&appid={settings.API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        response_json = response.json()
        return response_json
