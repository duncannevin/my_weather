from typing import Literal

from pydantic import BaseModel, Field


class WeatherQuery(BaseModel):
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude")
    units: Literal["metric", "imperial"] = Field(..., description="Units")
