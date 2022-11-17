from typing import Optional
from uuid import UUID

from pydantic import validator

from app.core.utils.geoposition import get_coordinates
from app.models.base import BaseSchema


class CityBase(BaseSchema):
    name: str
    latitude: Optional[float]
    longitude: Optional[float]

    @validator("name")
    def city_is_exist(cls, v):
        coordinates = get_coordinates(v)
        if coordinates.not_exists:
            raise ValueError('Entered city not exist')
        return v

    @classmethod
    def init_coordinates(cls):
        coordinates = get_coordinates(cls.name)
        cls.longitude = coordinates.longitude
        cls.latitude = coordinates.latitude


class CityIn(CityBase):
    id: Optional[UUID]


class CityOut(CityBase):
    id: UUID
