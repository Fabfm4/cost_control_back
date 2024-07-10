import os
from typing import TypeVar


primaryKey = TypeVar('primaryKey')


class MixinConnection():

    entity_name = None

    async def __init__(self) -> None:
        if not self.entity_name:
            raise NotImplementedError('entity_name is not defined')

        DB_URL_CONNECTION = os.environ.get('DB_URL_CONNECTION', None)
        DB_DATABASE = os.environ.get('DB_DATABASE', None)

        if not DB_URL_CONNECTION or not DB_DATABASE:
            raise NotImplementedError(
                'DB_URL_CONNECTION or DB_DATABASE is not defined')

        self.connection = await self.__connect(DB_URL_CONNECTION, DB_DATABASE)

    async def __connect(self, URL: str, DATABASE: str):
        raise NotImplementedError

    @classmethod
    async def count_query(cls, query: dict = {}):
        raise NotImplementedError

    @classmethod
    async def query(cls, query: dict = {}):
        raise NotImplementedError

    @classmethod
    async def query_index(cls, query: dict = {}):
        raise NotImplementedError

    @classmethod
    async def create(cls, model_data: dict) -> bool:
        raise NotImplementedError

    @classmethod
    async def update(cls, primary_key: primaryKey, object_data: dict):
        raise NotImplementedError
