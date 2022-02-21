from sqlalchemy import Column, String, Enum, DateTime, Boolean, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID

from src.api.users.enums import UserRole, UserState
from src.app import DB
from src.repo.base_models import BaseDateTimeModel
from src.repo.sa_types import SqlalchemyTypesMixin

__all__ = [
    "UserORM",
]


class UserORM(DB, SqlalchemyTypesMixin, BaseDateTimeModel):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)

    login = Column(String, nullable=False, unique=True,)
    email = Column(String, nullable=False, unique=True,)

    firstname = Column(String, nullable=False,)
    lastname = Column(String, nullable=False,)
    surname = Column(String, nullable=True,)

    role = Column(Enum(UserRole), nullable=True, default=UserRole.student,)

    password_hash = Column(String, nullable=False,)
    expire_date = Column(DateTime, nullable=True,)
    state = Column(Enum(UserState), nullable=True, default=UserState.active,)


class UserGroupORM(DB, SqlalchemyTypesMixin, BaseDateTimeModel):
    __tablename__ = "users_groups"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True,)
    author_id = Column(UUID(as_uuid=True), nullable=False,)
    curator_id = Column(UUID(as_uuid=True), nullable=False,)

    title = Column(String, nullable=False,)
    description = Column(String, nullable=True,)

    __table_args__ = (
        ForeignKeyConstraint(("author_id",), ["users.id"], ondelete="RESTRICT", name="__author_id_fk"),
        ForeignKeyConstraint(("curator_id",), ["users.id"], ondelete="RESTRICT", name="__curator_id_fk"),
    )


class UserGroupRelationORM(DB, SqlalchemyTypesMixin, BaseDateTimeModel):
    __tablename__ = "users_groups_relations"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True,)
    user_id = Column(UUID(as_uuid=True), nullable=False,)
    user_group_id = Column(UUID(as_uuid=True), nullable=False)

    is_head_of_group = Column(Boolean, nullable=False, default=False)

    __table_args__ = (
        ForeignKeyConstraint(("user_id",), ["users.id"], ondelete="CASCADE", name="__author_id_fk"),
        ForeignKeyConstraint(("user_group_id",), ["users_groups.id"], ondelete="CASCADE", name="__user_group_id_fk"),

    )

