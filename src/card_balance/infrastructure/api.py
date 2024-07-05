from bson import ObjectId
from bson.objectid import InvalidId

from fastapi import APIRouter

from core.infrastructure.db import raise_404_error
from card_balance.app import get_balance_by_card_id

from core.domain import bModel, get_collection_model
from card_balance.domain import CardBalanceModel
from card_balance.infrastructure.db import CardBalanceDB


router = APIRouter(
    prefix="/card_balance",
    tags=["card_balance"],
    responses={404: {"description": "Not found"}},
)


CollectionModel: type[bModel] = get_collection_model(CardBalanceModel)


@router.get(
    "/{card_id}",
    response_description="Get a single transaction",
    response_model=CardBalanceModel,
    response_model_by_alias=False)
async def get_transaction_router(card_id: str):
    try:
        ObjectId(card_id)
        return await get_balance_by_card_id(
            card_id, CardBalanceDB.query_db, raise_404_error)

    except InvalidId:
        raise_404_error('transaction', card_id)
