from datetime import datetime
from typing import Callable, NewType
from pydantic import BaseModel, ConfigDict, Field


from src.core.domain.core_domain import _CatalogModel

TModel = NewType('T', BaseModel)
callableGetRetrive = NewType('callableGetRetrive', Callable)


class BankModel(_CatalogModel):

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class BankModelInsert(BaseModel):
    name: str
    is_active: bool = True


class BankModelCreate(BankModelInsert):
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = None


class BankModelUpdate(BankModelInsert):
    updated_at: datetime = Field(default_factory=lambda: datetime.now())


class BankModelRequest(BaseModel):
    name: str
