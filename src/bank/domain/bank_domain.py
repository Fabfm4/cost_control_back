from pydantic import ConfigDict

from src.core.domain.core_domain import _CatalogModel


class BankModel(_CatalogModel):

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
