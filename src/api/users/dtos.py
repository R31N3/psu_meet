import datetime
from typing import Optional, List, Tuple
from uuid import UUID

from pydantic import BaseModel, validator

from src.api.users.enums import UserRole

__all__ = ["CreateUserFAPI"]

from src.api.users.service import get_password_hash
from src.repo.base_validators import datetime_validator


class CreateUserFAPI(BaseModel):
    login: str
    email: str

    firstname: str
    lastname: str
    surname: Optional[str]

    role: UserRole

    password: str

    expire_date: Optional[datetime.datetime]

    @validator("password", pre=True, always=True)
    def hash_password(cls, var):  # noqa
        return get_password_hash(var)

    @validator("expire_date", pre=True, always=True)
    def validate_expire_date(cls, var):  # noqa
        return datetime_validator(var)


class CreateUserGroupFAPI(BaseModel):
    curator_id: Optional[UUID]

    title: str
    description: str

    group_users_info: List[Tuple[UUID, bool]]
