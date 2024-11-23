from typing import Optional

from pydantic import BaseModel


class Wind(BaseModel):
    speed: float
    deg: int
    gust: Optional[float] = None
