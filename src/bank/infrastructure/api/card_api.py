from fastapi import APIRouter, Body, status

from src.core.domain.core_domain import T, get_collection_model
from src.bank.infrastructure.db.card_db import CardDB
from src.bank.domain.card_domain import CardModel, CardModelUpdate


router = APIRouter(
    prefix="/cards",
    tags=["cards"],
    responses={404: {"description": "Not found"}},
)


CollectionModel: type[T] = get_collection_model(CardModel)


@router.get(
        "/",
        response_description="List all cards",
        response_model=CollectionModel,
        response_model_by_alias=False,
        )
async def list_cards():
    card_data = await CardDB().get_all()
    collection_demo = CollectionModel(data=card_data)
    return collection_demo


@router.post(
        "/",
        response_description="Create a new card",
        response_model=CardModel,
        response_model_by_alias=False,
        status_code=status.HTTP_201_CREATED,
        )
async def create_card(card: CardModel = Body(...)):
    db_object = CardDB()
    card._set_created_at()
    card_created = await db_object.create(card)
    return await db_object.get_one(card_created.inserted_id)


@router.get(
        "/{card_id}",
        response_description="Get a single card",
        response_model=CardModel,
        response_model_by_alias=False,
        )
async def get_card(card_id: str):
    return await CardDB().get_one(card_id)


@router.put(
        "/{card_id}",
        response_description="Update a card",
        response_model=CardModelUpdate,
        response_model_by_alias=False,
        )
async def update_card(card_id: str, card: CardModelUpdate = Body(...)):
    db_object = CardDB()
    card_object = await db_object.get_one(card_id)
    card._set_updated_at()
    data_raw = {k: v for k, v in card.model_dump(by_alias=True).items() if v is not None}
    if data_raw:
        return await CardDB().update(card_id, data_raw)

    return card_object
