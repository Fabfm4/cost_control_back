

import motor
from pymongo import ReturnDocument
from app.core.infrastructure.db.conection_hints import MixinConnection
from .conection_hints import primaryKey


class MongoDB(MixinConnection):

    async def __connect(self, URL: str, DATABASE: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(URL)
        self.db = getattr(self.client, DATABASE)
        self.collection = self.db.get_collection(self.entity_name)

    @classmethod
    async def count_query(cls, query: dict = {}):
        return await cls().collection.count_documents(query)

    @classmethod
    async def query(cls, query: dict = {}):
        query_solution = cls().collection.find(query)
        return await query_solution.to_list(length=None)

    @classmethod
    async def query_index(cls, query: dict = {}):
        return await cls().collection.find_one(query)

    @classmethod
    async def create(cls, model_data: dict) -> bool:
        return await cls().collection.insert_one(model_data)

    @classmethod
    async def update(cls, primary_key: primaryKey, object_data: dict):
        return await cls().collection.find_one_and_update(
            {"_id": primary_key},
            {"$set": object_data},
            return_document=ReturnDocument.AFTER
        )
