from typing import List

from bson import ObjectId
from core.application import (
    create_mixin,
    delete_mixin,
    get_mixin,
    list_mixin,
    update_mixin
)
from transaction.domain import (
    TransactionModel,
    TransactionModelMandatoryRequest,
    TransactionModelUpdate,
    TransactionModelUpdateRequest
)
from core.domain import (
    callableListDataModel,
    callableUpdateDataModel,
    callableCreateDataModel,
    callable404Error
)


async def list_transaction(
        card_id: str,
        list_db_transaction_callable: callableListDataModel
        ) -> List[TransactionModel]:
    return await list_mixin(list_db_transaction_callable, {"card_id": card_id})


async def get_transaction(
        pk: ObjectId,
        get_db_transaction_callable: callableListDataModel,
        raise_404_error: callable404Error
        ) -> TransactionModel:
    return await get_mixin(pk, get_db_transaction_callable, raise_404_error)


async def create_transaction(
        transaction_data: TransactionModelMandatoryRequest,
        create_db_transaction_callable: callableCreateDataModel,
        get_db_transaction_callable: callableListDataModel
        ) -> TransactionModel:
    return await create_mixin(
        transaction_data,
        create_db_transaction_callable,
        get_db_transaction_callable,
        TransactionModel)


async def update_transaction(
        pk: ObjectId,
        transaction_data_update: TransactionModelUpdateRequest,
        count_db_transaction_callable: callableListDataModel,
        update_db_transaction_callable: callableUpdateDataModel,
        raise_404_error: callable404Error
        ) -> TransactionModel:
    return await update_mixin(
        pk, transaction_data_update,
        count_db_transaction_callable, update_db_transaction_callable,
        raise_404_error, TransactionModelUpdate
    )


async def delete_transaction(
        pk: ObjectId,
        get_db_transaction_callable: callableListDataModel,
        update_db_transaction_callable: callableUpdateDataModel,
        raise_404_error: callable404Error
        ) -> None:
    return await delete_mixin(
        pk, get_db_transaction_callable,
        update_db_transaction_callable, raise_404_error)
