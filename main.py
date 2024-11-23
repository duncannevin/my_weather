from core.init import initialize

from routes import weather
from starlette.staticfiles import StaticFiles

app = initialize()

app.include_router(weather.router)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/", StaticFiles(directory="frontend/views", html=True), name="static")
