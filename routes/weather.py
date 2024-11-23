from typing import Annotated

from fastapi import Query, Body, APIRouter

from cache import cache, redis_client
from services.weather import *

router = APIRouter()


@router.get("/weather/forecast")
@cache(redis_client)
async def weather_forecast(
    cnt = Query(...),
    lat = Query(...),
    lon = Query(...),
    units = Query(...),
):
    query_params = ForecastQueryParams(
        cnt=cnt,
        lat=lat,
        lon=lon,
        units=units,
    )
    return await fetch_forecast(query_params)


@router.post("/weather")
async def weather(data: Annotated[WeatherQuery, Body()]) -> WeatherResponse:
    return await fetch_weather(data)
