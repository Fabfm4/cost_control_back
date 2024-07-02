from bson import ObjectId
from bson.objectid import InvalidId

from fastapi import APIRouter, Body, status

from core.infrastructure.db import raise_404_error
from transaction.app import (
    create_transaction, list_transaction,
    get_transaction, update_transaction,
    delete_transaction)
from core.domain import bModel, get_collection_model
from transaction.infrastructure.db import TransactionDB
from transaction.domain import (
    TransactionModel,
    TransactionModelMandatoryRequest,
    TransactionModelUpdateRequest
)


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)


CollectionModel: type[bModel] = get_collection_model(TransactionModel)


@router.get(
        "/",
        response_description="List all transactions",
        response_model=CollectionModel,
        response_model_by_alias=False
        )
async def list_transaction_router(card_id: str, q: str = None):
    print(card_id, q)
    return CollectionModel(data=await list_transaction(
        card_id, TransactionDB.query_db))


@router.post(
        "/",
        response_description="Create a new transaction",
        response_model=TransactionModel,
        response_model_by_alias=False,
        status_code=status.HTTP_201_CREATED,
        )
async def create_transaction_router(
        transaction: TransactionModelMandatoryRequest = Body(...)):
    return await create_transaction(
        transaction, TransactionDB.create, TransactionDB.query_db)


@router.get(
        "/{pk}",
        response_description="Get a single transaction",
        response_model=TransactionModel,
        response_model_by_alias=False,
        )
async def get_transaction_router(pk: str):
    try:
        _id = ObjectId(pk)
        return await get_transaction(
            _id, TransactionDB.query_db, raise_404_error)

    except InvalidId:
        raise_404_error('transaction', pk)


@router.put(
        "/{pk}",
        response_description="Update a transaction",
        response_model=TransactionModel,
        response_model_by_alias=False,
        )
async def update_transaction_router(
        pk: str, transaction: TransactionModelUpdateRequest = Body(...)):
    try:
        _id = ObjectId(pk)
        return await update_transaction(
            _id, transaction, TransactionDB.count_query_db,
            TransactionDB.update, raise_404_error)

    except InvalidId:
        raise_404_error('transaction', pk)


@router.delete(
    '/{pk}',
    response_description="Delete a transaction"
    )
async def delete_transaction_router(pk: str):
    try:
        _id = ObjectId(pk)
        return await delete_transaction(
            _id, TransactionDB.query_db,
            TransactionDB.update, raise_404_error)

    except InvalidId:
        raise_404_error('transaction', pk)
