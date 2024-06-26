from typing import List

from bson import ObjectId
from src.bank.domain.bank_domain import (
    BankModel,
    BankModelRequest,
    BankModelUpdate,
    BankModelCreate)
from src.core.domain.core_domain import (
    callableListDataModel,
    callableUpdateDataModel,
    callableCreateDataModel,
    callable404Error
)


async def list_bank(
        list_db_bank_callable: callableListDataModel
        ) -> List[BankModel]:
    return await list_db_bank_callable({"is_active": True})


async def get_bank(
        pk: ObjectId,
        get_db_bank_callable: callableListDataModel,
        raise_404_error: callable404Error
        ) -> BankModel:
    bank_object = await get_db_bank_callable({'_id': pk})
    if not bank_object:
        raise_404_error('bank', str(pk))

    return BankModel(**bank_object[0])


async def create_bank(
        bank_data: BankModelRequest,
        create_db_bank_callable: callableCreateDataModel,
        get_db_bank_callable: callableListDataModel
        ) -> BankModel:
    bank_data = BankModelCreate(
        **bank_data.model_dump(by_alias=True))
    bank_object_creted = await create_db_bank_callable(
        bank_data.model_dump(by_alias=True))
    bank_object = await get_db_bank_callable(
        {'_id': bank_object_creted.inserted_id})
    return BankModel(**bank_object[0])


async def update_bank(
        pk: ObjectId,
        bank_data_update: BankModelRequest,
        count_db_bank_callable: callableListDataModel,
        update_db_bank_callable: callableUpdateDataModel,
        raise_404_error: callable404Error
        ) -> BankModel:
    if (await count_db_bank_callable({'_id': pk})) < 1:
        raise_404_error('bank', str(pk))

    bank_data_update = BankModelUpdate(
        **bank_data_update.model_dump(by_alias=True))
    bank_object = await update_db_bank_callable(
        pk, bank_data_update.model_dump(by_alias=True))
    return bank_object


async def delete_bank(
        pk: ObjectId,
        get_db_bank_callable: callableListDataModel,
        update_db_bank_callable: callableUpdateDataModel,
        raise_404_error: callable404Error
        ) -> None:
    bank_object = await get_db_bank_callable({'_id': pk})
    if not bank_object:
        raise_404_error('bank', str(pk))

    await update_db_bank_callable(pk, {"is_active": False})
