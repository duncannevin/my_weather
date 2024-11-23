from typing import Literal

from pydantic import Field, BaseModel


class ForecastQueryParams(BaseModel):
    cnt: int = Field(..., description="count")
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude")
    units: Literal["metric", "imperial"] = Field(..., description="Units")
