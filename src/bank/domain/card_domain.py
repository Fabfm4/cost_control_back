from enum import Enum
from typing import Optional
from pydantic import ConfigDict, Field

from src.core.domain.core_domain import _CatalogModel, PyObjectId


class CardTypeEnum(str, Enum):
    CREDIT = 'credit'
    DEBIT = 'debit'


class CardModel(_CatalogModel):
    bank_id: Optional[PyObjectId] = Field(alias='_bank_id', default=None)

    last_digits: str = Field(...)
    card_type: CardTypeEnum = Field(...)
    deadline_payment: int = Field(...)
    cutoff_day_payment: int = Field(...)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class CardModelUpdate(_CatalogModel):
    name: Optional[str] = None
    bank_id: Optional[PyObjectId] = None
    last_digits: Optional[str] = None
    card_type: Optional[CardTypeEnum] = None
    deadline_payment: Optional[int] = None
    cutoff_day_payment: Optional[int] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
