from pydantic import BaseModel


class Weather(BaseModel):
    id: int
    main: str
    description: str
    icon: str

