from sqlalchemy.sql import func

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr


__all__ = ["BaseDateTimeModel"]


class BaseDateTimeModel(object):
    @declared_attr
    def created_at(cls):
        return Column(DateTime(), nullable=False, server_default=func.current_timestamp())

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime(),
            nullable=False,
            server_default=func.current_timestamp(),
            onupdate=func.current_timestamp()
        )
