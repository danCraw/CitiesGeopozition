from typing import Type

import sqlalchemy

from app.db.repositories.base import BaseRepository
from app.db.tables.cities import City
from app.models.city import CityIn, CityOut


class CityRepository(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return City

    @property
    def _schema_out(self) -> Type[CityOut]:
        return CityOut

    @property
    def _schema_in(self) -> Type[CityIn]:
        return CityIn
