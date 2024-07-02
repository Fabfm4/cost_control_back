
from pydantic import ConfigDict, Field

from core.domain import PyObjectId, _RawModel


class CardBalanceModel(_RawModel):
    total_balance: float = Field(...)
    card_id: PyObjectId = Field(...)
    month: int = Field(...)
    initial_day: int = Field(...)
    final_day: int = Field(...)
    year: int = Field(...)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
