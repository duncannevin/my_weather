from typing import Optional

from pydantic import BaseModel


class System(BaseModel):
    type: Optional[int] = None
    id: Optional[int] = None
    country: Optional[str] = None
    sunrise: int
    sunset: int

