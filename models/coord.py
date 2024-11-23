from pydantic import BaseModel


class Coord(BaseModel):
    lon: float
    lat: float
