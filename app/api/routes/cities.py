from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.core.config import config
from app.core.utils.cities import get_more_close_cities
from app.db.repositories.cities import CityRepository
from app.models.city import CityIn, CityOut

router = APIRouter()


@router.get("/")
async def cities_list() -> List[CityOut]:
    city_repo: CityRepository = CityRepository()
    city = await city_repo.list()
    return city


@router.get("/{id}")
async def one_city(city_id: UUID) -> CityOut:
    city_repo: CityRepository = CityRepository()
    city = await city_repo.get(city_id)
    if city:
        return city
    else:
        raise HTTPException(status_code=404, detail="city with the given Id not found")


@router.post("/")
async def create_city(city: CityIn) -> CityOut:
    city_repo: CityRepository = CityRepository()
    city.init_coordinates()
    city = await city_repo.create(city)
    return city


@router.put("/")
async def update_city(city: CityIn) -> CityOut:
    city_repo: CityRepository = CityRepository()
    city = await city_repo.update(city)
    if city:
        return city
    else:
        raise HTTPException(status_code=404, detail="city with the given Id not found")


@router.delete("/{id}")
async def delete_city(city_id: UUID) -> List[CityOut]:
    city_repo: CityRepository = CityRepository()
    city = await city_repo.delete(city_id)
    if city:
        return city
    else:
        raise HTTPException(status_code=404, detail="city with the given Id not found")


@router.get("/close_cities/{id}")
async def more_close_cities(city_id: UUID) -> List[CityOut | None]:
    city_repo: CityRepository = CityRepository()
    cities = await city_repo.list()
    central_city = await city_repo.get(city_id)
    return get_more_close_cities(central_city, cities, config.amount_close_cities)
