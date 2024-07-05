from typing import List

from bson import ObjectId
from core.application import (
    create_mixin,
    delete_mixin,
    get_mixin,
    list_mixin,
    update_mixin
)
from bank.domain import (
    BankModel,
    BankModelMandatoryRequest,
    BankModelUpdate,
    BankModelUpdateRequest
)
from core.domain import (
    callableListDataModel,
    callableUpdateDataModel,
    callableCreateDataModel,
    callable404Error
)


async def list_bank(
        list_db_bank_callable: callableListDataModel) -> List[BankModel]:
    return await list_mixin(list_db_bank_callable, {"is_active": True})


async def get_bank(
        pk: ObjectId,
        get_db_bank_callable: callableListDataModel,
        raise_404_error: callable404Error) -> BankModel:
    return await get_mixin(pk, get_db_bank_callable, raise_404_error)


async def create_bank(
        bank_data: BankModelMandatoryRequest,
        create_db_bank_callable: callableCreateDataModel,
        get_db_bank_callable: callableListDataModel) -> BankModel:
    return await create_mixin(
        bank_data,
        create_db_bank_callable,
        get_db_bank_callable,
        BankModel)


async def update_bank(
        pk: ObjectId,
        bank_data_update: BankModelUpdateRequest,
        count_db_bank_callable: callableListDataModel,
        update_db_bank_callable: callableUpdateDataModel,
        raise_404_error: callable404Error) -> BankModel:
    return await update_mixin(
        pk, bank_data_update, count_db_bank_callable, update_db_bank_callable,
        raise_404_error, BankModelUpdate
    )


async def delete_bank(
        pk: ObjectId,
        get_db_bank_callable: callableListDataModel,
        update_db_bank_callable: callableUpdateDataModel,
        raise_404_error: callable404Error) -> None:
    return await delete_mixin(
        pk, get_db_bank_callable, update_db_bank_callable, raise_404_error)
