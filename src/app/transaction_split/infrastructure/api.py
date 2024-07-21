from bson import ObjectId
from bson.objectid import InvalidId

from fastapi import APIRouter, Body, status

from app.core.infrastructure.api.utils import raise_404_error
from app.transaction_split.app import (
    create_transaction_split, list_transaction_split,
    get_transaction_split, update_transaction_split,
    delete_transaction_split)
from app.core.domain import bModel, get_collection_model
from app.transaction_split.infrastructure.db import TransactionSplitDB
from app.transaction_split.domain import (
    TransactionSplitModel,
    TransactionSplitModelMandatoryRequest,
    TransactionSplitModelUpdateRequest
)


router = APIRouter(
    prefix="/transaction_splits",
    tags=["transaction_splits"],
    responses={404: {"description": "Not found"}},
)


CollectionModel: type[bModel] = get_collection_model(TransactionSplitModel)


@router.get(
    "/",
    response_description="List all transactions split",
    response_model=CollectionModel,
    response_model_by_alias=False)
async def list_transaction_split_router(card_id: str, q: str = None):
    return CollectionModel(data=await list_transaction_split(
        card_id, TransactionSplitDB.query))


@router.post(
    "/",
    response_description="Create a new transactions split",
    response_model=TransactionSplitModel,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED)
async def create_transaction_split_router(
        transaction_split: TransactionSplitModelMandatoryRequest = Body(...)):
    return await create_transaction_split(
        transaction_split,
        TransactionSplitDB.create,
        TransactionSplitDB.query)


@router.get(
    "/{pk}",
    response_description="Get a single transactions split",
    response_model=TransactionSplitModel,
    response_model_by_alias=False)
async def get_transaction_split_router(pk: str):
    try:
        _id = ObjectId(pk)
        return await get_transaction_split(
            _id, TransactionSplitDB.query, raise_404_error)

    except InvalidId:
        raise_404_error('transaction_split', pk)


@router.put(
    "/{pk}",
    response_description="Update a transactions split",
    response_model=TransactionSplitModel,
    response_model_by_alias=False)
async def update_transaction_split_router(
        pk: str,
        transaction_split: TransactionSplitModelUpdateRequest = Body(...)):
    try:
        _id = ObjectId(pk)
        return await update_transaction_split(
            _id, transaction_split, TransactionSplitDB.count_query,
            TransactionSplitDB.update, raise_404_error)

    except InvalidId:
        raise_404_error('transaction_split', pk)


@router.delete(
    '/{pk}',
    response_description="Delete a transactions split")
async def delete_transaction_split_router(pk: str):
    try:
        _id = ObjectId(pk)
        return await delete_transaction_split(
            _id, TransactionSplitDB.query,
            TransactionSplitDB.update, raise_404_error)

    except InvalidId:
        raise_404_error('transaction_split', pk)
