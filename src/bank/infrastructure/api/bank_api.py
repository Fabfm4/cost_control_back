from fastapi import APIRouter, Body, HTTPException, status

from src.core.domain.core_domain import T, get_collection_model
from src.bank.infrastructure.db.bank_db import BankDB
from src.bank.domain.bank_domain import BankModel


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
        response_model_by_alias=False,
        )
async def list_banks():
    bank_data = await BankDB().get_all()
    collection_demo = CollectionModel(data=bank_data)
    return collection_demo


@router.post(
        "/",
        response_description="Create a new bank",
        response_model=BankModel,
        response_model_by_alias=False,
        status_code=status.HTTP_201_CREATED,
        )
async def create_bank(bank: BankModel = Body(...)):
    db_object = BankDB()
    bank_created = await db_object.create(bank)
    return await db_object.get_one(bank_created.inserted_id)

@router.get(
        "/{bank_id}",
        response_description="Get a single bank",
        response_model=BankModel,
        response_model_by_alias=False,
        )
async def get_bank(bank_id: str):
    return await BankDB().get_one(bank_id)


@router.put(
        "/{bank_id}",
        response_description="Update a bank",
        response_model=BankModel,
        response_model_by_alias=False,
        )
async def update_bank(bank_id: str, bank: BankModel = Body(...)):
    db_object = BankDB()
    bank_object = await db_object.get_one(bank_id)
    bank._set_updated_at()
    data_raw = {k: v for k, v in bank.model_dump(by_alias=True).items() if v is not None}
    if data_raw:
        return await BankDB().update(bank_id, data_raw)

    return bank_object
