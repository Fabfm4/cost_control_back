from datetime import datetime
from core.application import (
    list_mixin,
)
from card_balance.domain import (
    CardBalanceModel,
)

from core.domain import (
    callableListDataModel,
    callable404Error
)


async def get_balance_by_card_id(
        card_id: str,
        get_db_balance_callable: callableListDataModel,
        raise_404_error: callable404Error
        ) -> CardBalanceModel:
    current_date = datetime.now()
    day = current_date.day
    month = current_date.month
    year = current_date.year
    balance_list = await list_mixin(
        get_db_balance_callable,
        {
            "card_id": card_id,
            "month": month,
            "year": year
        }
    )
    if not balance_list:
        raise_404_error('object', str(card_id))

    return balance_list[0] if balance_list else None
