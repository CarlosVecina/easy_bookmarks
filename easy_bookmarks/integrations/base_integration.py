from abc import ABC, abstractmethod
from typing import Any

import polars as pl
from pydantic import BaseModel, RootModel, model_serializer

from easy_bookmarks.stores.utils import generate_uuid


class BaseBookmark(BaseModel):
    uuid: str | None = None
    uuid_fields: list[str]

    def __init__(self, **data):
        super().__init__(**data)
        if not self.uuid:
            self.uuid = generate_uuid(
                f"{''.join([self.model_dump()[i] for i in self.uuid_fields])}"
            )

    @model_serializer
    def ser_model(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if k != "uuid_fields"}


class BaseListBookmarks(RootModel):
    root: list[BaseBookmark]

    def to_polars_dataframe(self) -> pl.DataFrame:
        return pl.DataFrame([bookmark.model_dump() for bookmark in self.root])


class BaseIntegration(ABC, BaseModel):
    @abstractmethod
    def get_bookmarks(self) -> list[dict[str, Any]]: ...

    @abstractmethod
    def get_bookmarks_df(self) -> pl.DataFrame: ...
