from typing import List

from pydantic import BaseModel

from models import Coord, Weather, WeatherMain, Wind, Clouds, System


class WeatherResponse(BaseModel):
    coord: Coord
    weather: List[Weather]
    base: str
    main: WeatherMain
    visibility: int
    wind: Wind
    clouds: Clouds
    dt: int
    sys: System
    timezone: int
    id: int
    name: str
    cod: int

