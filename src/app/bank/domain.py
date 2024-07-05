from datetime import datetime
from typing import Callable, NewType, Optional
from pydantic import BaseModel, ConfigDict, Field


from app.core.domain import _CatalogModel

TModel = NewType('T', BaseModel)
callableGetRetrive = NewType('callableGetRetrive', Callable)


class BankModelMandatoryRequest(BaseModel):
    name: str = Field(...)


class BankModelUpdateRequest(BaseModel):
    name: Optional[str] = Field(...)


class BankModelUpdate(BankModelUpdateRequest):
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now())


class BankModel(_CatalogModel):

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )