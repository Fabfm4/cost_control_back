import asyncio
from typing import List

from bson import ObjectId
from app.card.domain import CardModel
from app.card_balance.app import compute_balance_by_card_id
from app.core.application import (
    create_mixin,
    delete_mixin,
    get_mixin,
    list_mixin,
    update_mixin
)
from app.transaction.domain import (
    TransactionModel,
    TransactionModelMandatoryRequest,
    TransactionModelUpdate,
    TransactionModelUpdateRequest
)
from app.core.domain import (
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
        raise_404_error: callable404Error) -> TransactionModel:
    return await get_mixin(pk, get_db_transaction_callable, raise_404_error)


async def create_transaction(
    transaction_data: TransactionModelMandatoryRequest,
    create_db_transaction_callable: callableCreateDataModel,
    get_db_transaction_callable: callableListDataModel,
    get_db_card_callable: callableListDataModel,
    get_db_balance_callable: callableListDataModel,
    create_db_balance_callable: callableCreateDataModel,
    update_db_balance_callable: callableUpdateDataModel
) -> TransactionModel:
    new_transaction = await create_mixin(
        transaction_data,
        create_db_transaction_callable,
        get_db_transaction_callable,
        TransactionModel)
    card = await get_db_card_callable(
        {"_id": ObjectId(transaction_data.card_id)})
    card_model = CardModel(**card)
    asyncio.create_task(
        compute_balance_by_card_id(
            card_model, new_transaction,
            get_db_balance_callable,
            update_db_balance_callable,
            create_db_balance_callable))

    return new_transaction


async def update_transaction(
        pk: ObjectId,
        transaction_data_update: TransactionModelUpdateRequest,
        count_db_transaction_callable: callableListDataModel,
        update_db_transaction_callable: callableUpdateDataModel,
        raise_404_error: callable404Error) -> TransactionModel:
    return await update_mixin(
        pk, transaction_data_update,
        count_db_transaction_callable, update_db_transaction_callable,
        raise_404_error, TransactionModelUpdate
    )


async def delete_transaction(
        pk: ObjectId,
        get_db_transaction_callable: callableListDataModel,
        update_db_transaction_callable: callableUpdateDataModel,
        raise_404_error: callable404Error) -> None:
    return await delete_mixin(
        pk, get_db_transaction_callable,
        update_db_transaction_callable, raise_404_error)
