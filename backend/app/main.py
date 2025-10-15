from fastapi import APIRouter, FastAPI

from app.routes.accums import app_accums
from app.routes.batteries import app_batteries


api_app = APIRouter(prefix="/api")
api_app.include_router(app_accums)
api_app.include_router(app_batteries)

app = FastAPI()
app.include_router(api_app)
