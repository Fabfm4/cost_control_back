from datetime import datetime

from bson import ObjectId


from card.domain import CardModel
from core.application import (
    list_mixin,
)
from card_balance.domain import (
    CardBalanceModel,
)

from core.domain import (
    callableListDataModel,
    callableUpdateDataModel,
    callableCreateDataModel,
    callable404Error
)
from transaction.domain import SPENDING, TransactionModel


async def get_balance_by_card_id(
        card_id: str,
        get_db_balance_callable: callableListDataModel,
        raise_404_error: callable404Error) -> CardBalanceModel:
    balance_list = await list_mixin(
        get_db_balance_callable,
        {"card_id": card_id}
    )
    if not balance_list:
        raise_404_error('object', str(card_id))

    return balance_list[0] if balance_list else None


async def compute_balance_by_card_id(
        card: CardModel,
        transaction: TransactionModel,
        get_db_balance_callable: callableListDataModel,
        update_db_balance_callable: callableUpdateDataModel,
        create_db_balance_callable: callableCreateDataModel,
        recalculate: bool = False) -> bool:
    transaction_month = transaction.date.month
    transaction_day = transaction.date.day
    card_cut_off = card.cutoff_day_payment
    transaction_year = transaction.date.year
    if card_cut_off <= transaction_day:
        transaction_month += 1

    if transaction_month > 12:
        transaction_month = 1
        transaction_year += 1

    amount = transaction.transaction_type == SPENDING and \
        transaction.amount or -transaction.amount

    balance = await get_db_balance_callable({
        "month": transaction_month,
        "year": transaction_year,
        "card_id": str(card.id)
    })
    if not balance:
        balance = await create_db_balance_callable({
            "month": transaction_month,
            "year": transaction_year,
            "card_id": str(card.id),
            "total_balance": amount,
            "initial_day": card.cutoff_day_payment,
            "payment_day": card.deadline_payment,
            "number_of_transactions": 1
        })
        return balance

    balance_model = CardBalanceModel(**balance)
    await update_db_balance_callable(
        ObjectId(balance_model.id),
        {
            "total_balance": balance_model.total_balance + amount,
            "number_of_transactions": balance_model.number_of_transactions + 1,
            "updated_at": datetime.now()
        }
    )
    return True
