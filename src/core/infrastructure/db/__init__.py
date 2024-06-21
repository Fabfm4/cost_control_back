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

    async def get_all(self) -> motor.motor_asyncio.AsyncIOMotorCursor:
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

    async def create(self, model: T) -> bool:
        data = model.model_dump(by_alias=True, exclude=["id"])
        return await self.collection.insert_one(data)

    def update(self, object_id: str, object_data: dict):
        try:
            _id = ObjectId(object_id)
            object_updated = self.collection.find_one_and_update(
                {"_id": _id},
                {"$set": object_data},
                return_document=ReturnDocument.AFTER
            )
            if object_updated:
                return object_updated
        except InvalidId:
            pass
        raise HTTPException(status_code=404, detail=f"Bank {object_id} not found")

    # def delete(self, user_id):
    #     return self.collection.delete_one({"_id": ObjectId(user_id)})