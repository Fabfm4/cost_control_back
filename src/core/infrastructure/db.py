import os

from typing import List, Tuple, TypeVar
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
        MONGODB_DBNAME = os.environ.get('MONGODB_DBNAME')
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
        self.db = getattr(self.client, MONGODB_DBNAME)
        self.collection = self.db.get_collection(
            self.collection_name)

    def _build_pipeline_one_to_one(pk: str, table_singular: str):
        mapping_field = f"{table_singular}_map"
        add_fields = {
            "$addFields": {
                f"obj_{table_singular}_id": {
                    "$toObjectId": f"${table_singular}_id"
                }
            }
        }
        match = {"$match": {"_id": ObjectId(pk)}}
        lookup = {
            "$lookup": {
                "from": f"{table_singular}s",
                "localField": f"obj_{table_singular}_id",
                "foreignField": "_id",
                "as": mapping_field
            }
        }
        only_one = {
            "$set": {f"{mapping_field}": {"$first": f"${mapping_field}"}}}
        return mapping_field, [match, add_fields, lookup, only_one]

    @classmethod
    async def count_query_db(cls, query: dict = {}):
        return await cls().collection.count_documents(query)

    @classmethod
    async def query_db(cls, query: dict = {}):
        query_solution = cls().collection.find(query)
        return await query_solution.to_list(length=None)

    @classmethod
    async def query_db_one(cls, query: dict = {}):
        return await cls().collection.find_one(query)

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

    @classmethod
    async def get_join_one_to_one(
            cls, pk: str, table_singular: str) -> Tuple[str, List]:
        super_class = cls()
        collection = super_class.collection
        field, pipeline = cls._build_pipeline_one_to_one(pk, table_singular)
        return field, await collection.aggregate(pipeline).to_list(length=None)


def raise_404_error(model_name: str, extra_message: str = ''):
    raise HTTPException(
        status_code=404, detail=f'{model_name} not found {extra_message}')
