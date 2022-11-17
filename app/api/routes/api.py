from fastapi import APIRouter

from app.api.routes import cities

api_router = APIRouter()

cities_router = APIRouter()
cities_router.include_router(cities.router, prefix="/cities")