from fastapi import APIRouter, FastAPI

from app.routes.accums import app_accums
from app.routes.devices import app_devices


api_app = APIRouter(prefix="/api")
api_app.include_router(app_accums)
api_app.include_router(app_devices)

app = FastAPI()
app.include_router(api_app)
