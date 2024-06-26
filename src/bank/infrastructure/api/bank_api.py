from bson import ObjectId
from bson.objectid import InvalidId

from fastapi import APIRouter, Body, status

from src.core.infrastructure.db import raise_404_error
from src.bank.application.bank_app import (
    create_bank, list_bank, get_bank, update_bank, delete_bank)
from src.core.domain.core_domain import T, get_collection_model
from src.bank.infrastructure.db.bank_db import BankDB
from src.bank.domain.bank_domain import (
    BankModel, BankModelRequest)


router = APIRouter(
    prefix="/banks",
    tags=["banks"],
    responses={404: {"description": "Not found"}},
)


CollectionModel: type[T] = get_collection_model(BankModel)


@router.get(
        "/",
        response_description="List all banks",
        response_model=CollectionModel,
        response_model_by_alias=False
        )
async def list_bank_router(q: str = None):
    bank_db_conn = BankDB()
    return CollectionModel(data=await list_bank(bank_db_conn.query_db))


@router.post(
        "/",
        response_description="Create a new bank",
        response_model=BankModel,
        response_model_by_alias=False,
        status_code=status.HTTP_201_CREATED,
        )
async def create_bank_router(bank: BankModelRequest = Body(...)):
    db_object = BankDB()
    return await create_bank(bank, db_object.create, db_object.query_db)


@router.get(
        "/{pk}",
        response_description="Get a single bank",
        response_model=BankModel,
        response_model_by_alias=False,
        )
async def get_bank_router(pk: str):
    try:
        _id = ObjectId(pk)
        bank_db_conn = BankDB()
        return await get_bank(
            _id, bank_db_conn.query_db, raise_404_error)

    except InvalidId:
        raise_404_error('bank', pk)


@router.put(
        "/{pk}",
        response_description="Update a bank",
        response_model=BankModel,
        response_model_by_alias=False,
        )
async def update_bank_router(pk: str, bank: BankModelRequest = Body(...)):
    try:
        _id = ObjectId(pk)
        bank_db_conn = BankDB()
        return await update_bank(
            _id, bank, bank_db_conn.count_query_db,
            bank_db_conn.update, raise_404_error)

    except InvalidId:
        raise_404_error('bank', pk)


@router.delete(
    '/{pk}',
    response_description="Delete a bank"
    )
async def delete_bank_router(pk: str):
    try:
        _id = ObjectId(pk)
        bank_db_conn = BankDB()
        return await delete_bank(
            _id, bank_db_conn.query_db,
            bank_db_conn.update, raise_404_error)

    except InvalidId:
        raise_404_error('bank', pk)
