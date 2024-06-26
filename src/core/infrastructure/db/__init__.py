import os

from typing import TypeVar
from bson import ObjectId
from bson.objectid import InvalidId
from fastapi import HTTPException
import motor.motor_asyncio
from pydantic import BaseModel
from pymongo import ReturnDocument

T = TypeVar('T', bound=BaseModel)


class MongoDBConection:

    collection_name = None
    base_model = None

    def __init__(self):
        MONGODB_URL = os.environ.get('MONGODB_URL')
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
        self.db = self.client.cost_db
        self.collection = self.db.get_collection(
            self.collection_name)

    async def count_query_db(self, query: dict = {}):
        return await self.collection.count_documents(query)

    async def query_db(self, query: dict = {}):
        query_solution = self.collection.find(query)
        return await query_solution.to_list(length=None)

    async def get_all(self) -> list[T]:
        return await self.collection.find().to_list(length=None)

    async def get_one(self, object_id: str):
        try:
            _id = ObjectId(object_id)
            object_raw = await self.collection.find_one({"_id": _id})
            if object_raw:
                return object_raw
        except InvalidId:
            pass

        raise HTTPException(status_code=404, detail=f"Bank {object_id} not found")

    async def create(self, model_data: dict) -> bool:
        return await self.collection.insert_one(model_data)

    def update(self, object_id: ObjectId, object_data: dict):
        return self.collection.find_one_and_update(
            {"_id": object_id},
            {"$set": object_data},
            return_document=ReturnDocument.AFTER
        )


async def mixin_list_objects(self):
    return await self.collection.find().to_list(length=None)


def raise_404_error(model_name: str, extra_message: str = ''):
    raise HTTPException(
        status_code=404, detail=f'{model_name} not found {extra_message}')
