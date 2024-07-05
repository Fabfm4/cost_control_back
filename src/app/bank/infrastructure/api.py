from bson import ObjectId
from bson.objectid import InvalidId

from fastapi import APIRouter, Body, status

from app.core.infrastructure.db import raise_404_error
from app.bank.app import (
    create_bank, list_bank, get_bank, update_bank, delete_bank)
from app.core.domain import bModel, get_collection_model
from app.bank.infrastructure.db import BankDB
from app.bank.domain import (
    BankModel,
    BankModelMandatoryRequest,
    BankModelUpdateRequest
)


router = APIRouter(
    prefix="/banks",
    tags=["banks"],
    responses={404: {"description": "Not found"}},
)


CollectionModel: type[bModel] = get_collection_model(BankModel)


@router.get(
    "/",
    response_description="List all banks",
    response_model=CollectionModel,
    response_model_by_alias=False)
async def list_bank_router(q: str = None):
    return CollectionModel(data=await list_bank(BankDB.query_db))


@router.post(
    "/",
    response_description="Create a new bank",
    response_model=BankModel,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED)
async def create_bank_router(bank: BankModelMandatoryRequest = Body(...)):
    return await create_bank(bank, BankDB.create, BankDB.query_db)


@router.get(
    "/{pk}",
    response_description="Get a single bank",
    response_model=BankModel,
    response_model_by_alias=False)
async def get_bank_router(pk: str):
    try:
        _id = ObjectId(pk)
        return await get_bank(
            _id, BankDB.query_db, raise_404_error)

    except InvalidId:
        raise_404_error('bank', pk)


@router.put(
    "/{pk}",
    response_description="Update a bank",
    response_model=BankModel,
    response_model_by_alias=False)
async def update_bank_router(
        pk: str, bank: BankModelUpdateRequest = Body(...)):
    try:
        _id = ObjectId(pk)
        return await update_bank(
            _id, bank, BankDB.count_query_db,
            BankDB.update, raise_404_error)

    except InvalidId:
        raise_404_error('bank', pk)


@router.delete(
    '/{pk}',
    response_description="Delete a bank")
async def delete_bank_router(pk: str):
    try:
        _id = ObjectId(pk)
        return await delete_bank(
            _id, BankDB.query_db,
            BankDB.update, raise_404_error)

    except InvalidId:
        raise_404_error('bank', pk)
