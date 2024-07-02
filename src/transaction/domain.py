

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from core.domain import PyObjectId, _RawModel


class TransactionTypeEnum(str, Enum):
    PAYMENT = 'paytment'
    SPENDING = 'spending'


class TransactionModelMandatoryRequest(BaseModel):
    amount: float = Field(...)
    card_id: PyObjectId = Field(...)
    transaction_type: TransactionTypeEnum = Field(...)
    description: str = None
    date: datetime = Field(default_factory=lambda: datetime.now())


class TransactionModelUpdateRequest(BaseModel):
    amount: Optional[float] = None
    card_id: Optional[PyObjectId] = Field(default=None)
    transaction_type: Optional[TransactionTypeEnum] = None
    description: Optional[str] = None
    date: Optional[datetime] = None


class TransactionModelUpdate(TransactionModelUpdateRequest):
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now())


class TransactionModel(_RawModel, TransactionModelMandatoryRequest):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
