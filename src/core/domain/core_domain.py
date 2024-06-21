from datetime import datetime

from typing import Annotated, Optional, Type, TypeVar

from pydantic import BaseModel, BeforeValidator, Field, ValidationError, field_validator, model_validator, root_validator, validator


def validate_timestamp(v, handler):
    if v == 'now':
        # we don't want to bother with further validation, just return the new value
        return datetime.now()
    try:
        return handler(v)
    except ValidationError:
        # validation failed, in this case we want to return a default value
        return datetime(2000, 1, 1)


PyObjectId = Annotated[str, BeforeValidator(str)]
T = TypeVar('T', bound=BaseModel)


class _RawModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    created_at: datetime = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

    def _set_updated_at(self):
        self.updated_at = datetime.now()

    def _set_created_at(self):
        self.created_at = datetime.now()


class _CatalogModel(_RawModel):
    name: str = Field(...)
    is_active: bool = Field(default=True)


def get_collection_model(base_model: type[T]) -> Type[T]:

    class CollectionModel(BaseModel):
        data: Optional[list[base_model]]
        current_page: int = Field(default=0)

    return CollectionModel
