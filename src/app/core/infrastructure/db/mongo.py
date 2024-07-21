

import motor.motor_asyncio
from pymongo import ReturnDocument

from app.core.infrastructure.db import primaryKey


class MongoDB():

    def __init__(self, URL: str, DATABASE: str, entity_name: str):
        self._connect(URL, DATABASE, entity_name)

    def _connect(self, URL: str, DATABASE: str, entity_name: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(URL)
        self.db = getattr(self.client, DATABASE)
        self.collection = self.db.get_collection(entity_name)

    async def count_query(self, query: dict = {}):
        return await self.collection.count_documents(query)

    async def query(self, query: dict = {}):
        qs = self.collection.find(query)
        return await qs.to_list(length=None)

    async def query_index(self, query: dict = {}):
        return await self.collection.find_one(query)

    async def create(self, model_data: dict) -> bool:
        return await self.collection.insert_one(model_data)

    async def update(self, primary_key: primaryKey, object_data: dict):
        return await self.collection.find_one_and_update(
            {"_id": primary_key},
            {"$set": object_data},
            return_document=ReturnDocument.AFTER
        )
