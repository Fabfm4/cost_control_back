

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.domain import PyObjectId, _RawModel


class TransactionSplitModelMandatoryRequest(BaseModel):
    total_amount: float = Field(...)
    months: int = Field(...)
    current_month: int = None
    rest_amount: float = None
    card_id: PyObjectId = Field(...)
    description: str = None
    day_apply: int = Field(...)


class TransactionSplitModelUpdateRequest(BaseModel):
    total_amount: Optional[float] = Field(default=None)
    months: Optional[int] = Field(default=None)
    current_month: Optional[int] = Field(default=None)
    rest_amount: Optional[float] = Field(default=None)
    card_id: Optional[PyObjectId] = Field(default=None)
    description: Optional[str] = Field(default=None)
    day_apply: Optional[int] = Field(default=None)


class TransactionSplitModelUpdate(TransactionSplitModelUpdateRequest):
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now())


class TransactionSplitModel(
        _RawModel, TransactionSplitModelMandatoryRequest):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
