from typing import List

from bson import ObjectId

from app.core.application import (
    create_mixin,
    delete_mixin,
    get_mixin,
    list_mixin,
    update_mixin
)
from app.card.domain import (
    CardModel,
    CardModelMandatoryRequest,
    CardModelUpdate,
    CardModelUpdateRequest)
from app.core.domain import (
    callableListDataModel,
    callableUpdateDataModel,
    callableCreateDataModel,
    callable404Error
)


async def list_card(
        list_db_card_callable: callableListDataModel) -> List[CardModel]:
    return await list_mixin(list_db_card_callable, {"is_active": True})


async def get_card(
        pk: ObjectId,
        get_db_card_callable: callableListDataModel,
        raise_404_error: callable404Error) -> CardModel:
    return await get_mixin(pk, get_db_card_callable, raise_404_error)


async def create_card(
        card_data: CardModelMandatoryRequest,
        create_db_card_callable: callableCreateDataModel,
        get_db_card_callable: callableListDataModel) -> CardModel:
    return await create_mixin(
        card_data,
        create_db_card_callable,
        get_db_card_callable,
        CardModel)


async def update_card(
        pk: ObjectId,
        card_data_update: CardModelUpdateRequest,
        count_db_card_callable: callableListDataModel,
        update_db_card_callable: callableUpdateDataModel,
        raise_404_error: callable404Error) -> CardModel:
    return await update_mixin(
        pk, card_data_update, count_db_card_callable, update_db_card_callable,
        raise_404_error, CardModelUpdate
    )


async def delete_card(
        pk: ObjectId,
        get_db_card_callable: callableListDataModel,
        update_db_card_callable: callableUpdateDataModel,
        raise_404_error: callable404Error) -> None:
    return await delete_mixin(
        pk, get_db_card_callable, update_db_card_callable, raise_404_error)
