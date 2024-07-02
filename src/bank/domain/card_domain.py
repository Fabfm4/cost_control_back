from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from core.domain import _CatalogModel, PyObjectId


class CardTypeEnum(str, Enum):
    CREDIT = 'credit'
    DEBIT = 'debit'


class CardModelMandatoryRequest(BaseModel):
    name: str = Field(...)
    bank_id: PyObjectId = Field(...)
    last_digits: str = Field(...)
    card_type: CardTypeEnum = Field(...)
    deadline_payment: int = Field(...)
    cutoff_day_payment: int = Field(...)


class CardModelUpdateRequest(BaseModel):
    name: Optional[str] = None
    bank_id: Optional[PyObjectId] = Field(default=None)
    last_digits: Optional[str] = None
    card_type: Optional[CardTypeEnum] = None
    deadline_payment: Optional[int] = None
    cutoff_day_payment: Optional[int] = None


class CardModelUpdate(CardModelUpdateRequest):
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now())


class CardModel(CardModelMandatoryRequest, _CatalogModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
