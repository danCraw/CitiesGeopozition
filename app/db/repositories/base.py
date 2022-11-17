import abc
from uuid import UUID, uuid4
from typing import Dict, List, Union

import databases
import sqlalchemy
from asyncpg import Record, UndefinedTableError

from app.db.base import database
from app.main import logger
from app.models.base import BaseSchema


class BaseRepository(abc.ABC):
    def __init__(self, db: databases.Database = database, *args, **kwargs) -> None:
        self._db = db
        super()

    @property
    @abc.abstractmethod
    def _table(self) -> sqlalchemy.Table:
        pass

    @property
    @abc.abstractmethod
    def _schema_out(self):
        pass

    @property
    @abc.abstractmethod
    def _schema_in(self):
        pass

    @staticmethod
    def generate_uuid() -> UUID:
        return uuid4()

    def _preprocess_create(self, values: Dict) -> Dict:
        if values.get('id', None) is None:
            values["id"] = self.generate_uuid()
        return values

    async def _list(self) -> List[Record]:
        query = self._table.select()
        try:
            return await self._db.fetch_all(query=query)
        except UndefinedTableError as e:
            logger.warning('Error' + str(e))
            raise e

    async def list(self) -> List:
        rows = await self._list()
        return [self._schema_out(**dict(dict(row).items())) for row in rows]

    async def create(self, values: Union[BaseSchema, Dict]) -> _schema_out:
        if isinstance(values, dict):
            values = self._schema_in(**values)
        dict_values = self._preprocess_create(dict(values))
        try:
            await self._db.execute(query=self._table.insert(), values=dict_values)
        except UndefinedTableError as e:
            logger.warning('Error' + str(e))
            raise e
        return self._schema_out(**dict_values)

    async def get(self, id: Union[int, UUID]) -> _schema_out:
        try:
            row = await self._db.fetch_one(query=self._table.select().where(self._table.c.id == id))
        except UndefinedTableError as e:
            logger.warning('Error' + str(e))
            raise e
        if row:
            return self._schema_out(**dict(dict(row).items()))
        else:
            return row

    async def update(self, values: Union[BaseSchema, Dict]) -> _schema_out:
        if isinstance(values, dict):
            values = self._schema_in(**values)
        dict_values = self._preprocess_create(dict(values))
        row = await self.get(dict_values['id'])
        if row:
            try:
                await self._db.execute(query=self._table.update().where(self._table.c.id == dict_values['id']),
                                       values=dict_values)
            except UndefinedTableError as e:
                logger.warning('Error' + str(e))
                raise e
            return self._schema_out(**dict_values)
        return row

    async def delete(self, id: Union[int, UUID]) -> _schema_out:
        row = await self.get(id)
        if row:
            try:
                await self._db.execute(query=self._table.delete().where(self._table.c.id == id))
            except UndefinedTableError as e:
                logger.warning('Error' + str(e))
                raise e
        return row
