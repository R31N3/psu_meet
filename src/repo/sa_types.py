from collections import Callable
from typing import Any

from sqlalchemy import MetaData, select as sa_select, update as sa_update, delete as sa_delete
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.dialects.postgresql.dml import insert as sa_pg_insert
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import Select, Update, Delete

__all__ = ["select", "insert", "update", "delete", "MetaDataPg", "SqlalchemyTypesMixin"]


select: Callable[[Any], Select] = sa_select
insert: Callable[[Any], Insert] = sa_pg_insert
update: Callable[[Any], Update] = sa_update
delete: Callable[[Any], Delete] = sa_delete


class MetaDataPg(MetaData):
    @property
    def bind(self) -> AsyncEngine:
        ...  # noqa


class SqlalchemyTypesMixin:
    metadata: MetaDataPg

    __table_args__: tuple

    def __init__(self, *args, **kwargs):
        ...  # noqa
