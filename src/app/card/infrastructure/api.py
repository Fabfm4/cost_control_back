from bson import ObjectId
from bson.objectid import InvalidId

from fastapi import APIRouter, Body, status

from app.core.infrastructure.db import raise_404_error
from app.card.app import (
    create_card, list_card, get_card, update_card, delete_card)
from app.core.domain import bModel, get_collection_model
from app.card.infrastructure.db import CardDB
from app.card.domain import (
    CardModel, CardModelMandatoryRequest, CardModelUpdateRequest
)


router = APIRouter(
    prefix="/cards",
    tags=["cards"],
    responses={404: {"description": "Not found"}},
)


CollectionModel: type[bModel] = get_collection_model(CardModel)


@router.get(
    "/",
    response_description="List all cards",
    response_model=CollectionModel,
    response_model_by_alias=False)
async def list_card_router():
    return CollectionModel(data=await list_card(CardDB.query_db))


@router.post(
    "/",
    response_description="Create a new card",
    response_model=CardModel,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED)
async def create_card_router(card: CardModelMandatoryRequest = Body(...)):
    return await create_card(card, CardDB.create, CardDB.query_db)


@router.get(
    "/{pk}",
    response_description="Get a single card",
    response_model=CardModel,
    response_model_by_alias=False)
async def get_card_router(pk: str):
    try:
        _id = ObjectId(pk)
        return await get_card(
            _id, CardDB.query_db, raise_404_error)

    except InvalidId:
        raise_404_error('card', pk)


@router.put(
    "/{pk}",
    response_description="Update a card",
    response_model=CardModel,
    response_model_by_alias=False)
async def update_card_router(
        pk: str, card: CardModelUpdateRequest = Body(...)):
    try:
        _id = ObjectId(pk)
        return await update_card(
            _id, card, CardDB.count_query_db,
            CardDB.update, raise_404_error)

    except InvalidId:
        raise_404_error('bank', pk)


@router.delete(
    '/{pk}',
    response_description="Delete a card")
async def delete_bank_router(pk: str):
    try:
        _id = ObjectId(pk)
        return await delete_card(
            _id, CardDB.query_db,
            CardDB.update, raise_404_error)

    except InvalidId:
        raise_404_error('card', pk)
