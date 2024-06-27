import os

from typing import TypeVar
from bson import ObjectId
from fastapi import HTTPException
import motor.motor_asyncio
from pydantic import BaseModel
from pymongo import ReturnDocument


T = TypeVar('T', bound=BaseModel)


class MongoDBConection:

    collection_name = None

    def __init__(self):
        MONGODB_URL = os.environ.get('MONGODB_URL')
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
        self.db = self.client.cost_db
        self.collection = self.db.get_collection(
            self.collection_name)

    @classmethod
    async def count_query_db(cls, query: dict = {}):
        return await cls().collection.count_documents(query)

    @classmethod
    async def query_db(cls, query: dict = {}):
        query_solution = cls().collection.find(query)
        return await query_solution.to_list(length=None)

    @classmethod
    async def create(cls, model_data: dict) -> bool:
        return await cls().collection.insert_one(model_data)

    @classmethod
    async def update(cls, object_id: ObjectId, object_data: dict):
        return await cls().collection.find_one_and_update(
            {"_id": object_id},
            {"$set": object_data},
            return_document=ReturnDocument.AFTER
        )


def raise_404_error(model_name: str, extra_message: str = ''):
    raise HTTPException(
        status_code=404, detail=f'{model_name} not found {extra_message}')
