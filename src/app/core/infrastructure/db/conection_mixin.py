import os

from app.core.infrastructure.db import primaryKey
from app.core.infrastructure.db.mongo import MongoDB


class MixinConnection():

    entity_name = None

    def __init__(self):
        if not self.entity_name:
            raise NotImplementedError('entity_name is not defined')

        DB_URL_CONNECTION = os.environ.get('DB_URL_CONNECTION', None)
        DB_DATABASE = os.environ.get('DB_DATABASE', None)
        DB_ENGINE = os.environ.get('DB_ENGINE', None)

        if not DB_URL_CONNECTION or not DB_DATABASE or not DB_ENGINE:
            raise NotImplementedError(
                'DB_URL_CONNECTION or DB_DATABASE or DB_ENGINE is not defined')

        if DB_ENGINE == 'mongo':
            self.engine = MongoDB(
                DB_URL_CONNECTION, DB_DATABASE, self.entity_name)

    @classmethod
    async def count_query(cls, query: dict = {}):
        engine = cls().engine
        return await engine.count_query(query)

    @classmethod
    async def query(cls, query: dict = {}):
        engine = cls().engine
        return await engine.query(query)

    @classmethod
    async def query_index(cls, query: dict = {}):
        engine = cls().engine
        return await engine.query_index(query)

    @classmethod
    async def create(cls, model_data: dict) -> bool:
        engine = cls().engine
        return await engine.create(model_data)

    @classmethod
    async def update(cls, primary_key: primaryKey, object_data: dict):
        engine = cls().engine
        return await engine.update(primary_key, object_data)

