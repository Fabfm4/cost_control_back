
from pydantic import ConfigDict, Field

from app.core.domain import PyObjectId, _RawModel


class CardBalanceModel(_RawModel):
    total_balance: float = Field(...)
    card_id: PyObjectId = Field(...)
    month: int = Field(...)
    initial_day: int = Field(...)
    payment_day: int = Field(...)
    year: int = Field(...)
    number_of_transactions: int = Field(...)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
