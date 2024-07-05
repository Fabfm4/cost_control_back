from typing import List

from bson import ObjectId
from core.application import (
    create_mixin,
    delete_mixin,
    get_mixin,
    list_mixin,
    update_mixin
)
from transaction_split.domain import (
    TransactionSplitModel,
    TransactionSplitModelMandatoryRequest,
    TransactionSplitModelUpdate,
    TransactionSplitModelUpdateRequest
)
from core.domain import (
    callableListDataModel,
    callableUpdateDataModel,
    callableCreateDataModel,
    callable404Error
)


async def list_transaction_split(
        card_id: str,
        list_db_transaction_split_callable: callableListDataModel
) -> List[TransactionSplitModel]:
    return await list_mixin(
        list_db_transaction_split_callable, {"card_id": card_id})


async def get_transaction_split(
        pk: ObjectId,
        get_db_transaction_split_callable: callableListDataModel,
        raise_404_error: callable404Error
) -> TransactionSplitModel:
    return await get_mixin(
        pk, get_db_transaction_split_callable, raise_404_error)


async def create_transaction_split(
        transaction_split_data: TransactionSplitModelMandatoryRequest,
        create_db_transaction_split_callable: callableCreateDataModel,
        get_db_transaction_split_callable: callableListDataModel
) -> TransactionSplitModel:
    return await create_mixin(
        transaction_split_data,
        create_db_transaction_split_callable,
        get_db_transaction_split_callable,
        TransactionSplitModel)


async def update_transaction_split(
        pk: ObjectId,
        transaction_split_data_update: TransactionSplitModelUpdateRequest,
        count_db_transaction_split_callable: callableListDataModel,
        update_db_transaction_split_callable: callableUpdateDataModel,
        raise_404_error: callable404Error
) -> TransactionSplitModel:
    return await update_mixin(
        pk, transaction_split_data_update,
        count_db_transaction_split_callable,
        update_db_transaction_split_callable,
        raise_404_error, TransactionSplitModelUpdate
    )


async def delete_transaction_split(
        pk: ObjectId,
        get_db_transaction_split_callable: callableListDataModel,
        update_db_transaction_split_callable: callableUpdateDataModel,
        raise_404_error: callable404Error
) -> None:
    return await delete_mixin(
        pk, get_db_transaction_split_callable,
        update_db_transaction_split_callable, raise_404_error)
