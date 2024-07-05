from datetime import datetime

from typing import Annotated, Callable, List, Optional, Tuple, Type, TypeVar

from pydantic import BaseModel, BeforeValidator, Field, ValidationError


PyObjectId = Annotated[str, BeforeValidator(str)]
bModel = TypeVar('bModel', bound=BaseModel)
base_upd_mod = TypeVar('base_upd_mod', bound=BaseModel)
bmrModel = TypeVar('bmrModel', bound=BaseModel)

query_set = TypeVar('query_set', bound=str)
callableListDataModel = Callable[
    [Optional[query_set], Optional[List]], List[bModel]]
callableCountListDataModel = Callable[[Optional[query_set]], int]
callableUpdateDataModel = Callable[[str, bModel], bModel]
callableCreateDataModel = Callable[[bModel], bModel]
callable404Error = Callable[[str, Optional[str]], None]
callableGetJoinOneDataModel = Callable[[str, str], Tuple[str, List]]


def validate_timestamp(v, handler):
    if v == 'now':
        # we don't want to bother with further validation,
        # just return the new value
        return datetime.now()
    try:
        return handler(v)
    except ValidationError:
        # validation failed, in this case we want to return a default value
        return datetime(2000, 1, 1)


class _RawModel(BaseModel):

    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default=None)


class _CatalogModel(_RawModel):
    name: str = Field(...)
    is_active: bool = Field(default=True)


def get_collection_model(base_model: type[bModel]) -> Type[bModel]:

    class CollectionModel(BaseModel):
        data: Optional[List[base_model]]
        current_page: int = Field(default=0)

    return CollectionModel
