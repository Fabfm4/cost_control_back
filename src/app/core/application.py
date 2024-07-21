from typing import List

from bson import ObjectId

from app.core.domain import (
    base_upd_mod,
    bModel,
    bmrModel,
    callableListDataModel,
    callableUpdateDataModel,
    callableCreateDataModel,
    callable404Error
)


async def list_mixin(
        list_db_callable: callableListDataModel,
        query: dict) -> List[bModel]:
    return await list_db_callable(query)


async def get_mixin(
        pk: ObjectId,
        get_db_callable: callableListDataModel,
        raise_404_error: callable404Error) -> bModel:
    object_ = await get_db_callable({'_id': pk})
    if not object_:
        raise_404_error('object', str(pk))

    return object_


async def create_mixin(
        data: bmrModel,
        create_db_callable: callableCreateDataModel,
        get_db_callable: callableListDataModel,
        ClassBaseModel: bModel) -> bModel:
    data = ClassBaseModel(
        **data.model_dump(by_alias=True))

    object_created = await create_db_callable(
        data.model_dump(by_alias=True, exclude=["id"]))
    object_ = await get_db_callable(
        {'_id': object_created.inserted_id})
    return ClassBaseModel(**object_[0])


async def update_mixin(
        pk: ObjectId,
        data_update: bmrModel,
        count_db_callable: callableListDataModel,
        update_db_callable: callableUpdateDataModel,
        raise_404_error: callable404Error,
        ClassBaseUpdateModel: base_upd_mod) -> bModel:
    if (await count_db_callable({'_id': pk})) < 1:
        raise_404_error('object', str(pk))

    data_update = ClassBaseUpdateModel(
        **data_update.model_dump(by_alias=True, exclude_none=True))
    return await update_db_callable(
        pk, data_update.model_dump(by_alias=True, exclude_none=True))


async def delete_mixin(
        pk: ObjectId,
        get_db_callable: callableListDataModel,
        update_db_callable: callableUpdateDataModel,
        raise_404_error: callable404Error) -> None:
    object_ = await get_db_callable({'_id': pk})
    if not object_:
        raise_404_error('object', str(pk))

    await update_db_callable(pk, {'is_active': False})
