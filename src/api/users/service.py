import datetime
import logging
from typing import Optional
from uuid import UUID

import asyncpg
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from jwt import PyJWTError
from passlib.context import CryptContext

from src.app import async_engine

__all__ = [
    "oauth2_scheme",
    "pwd_context",
    "get_password_hash",
    "create_access_token",
    "validate_token_dependency",
    "provide_auth",
    "get_current_user"
]

JWT_SECRET = "TEST"
JWT_ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/auth")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, password_hash) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> bytes:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(days=30)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return encoded_jwt


async def validate_token_dependency(token: str = Depends(oauth2_scheme),) -> None:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        username: Optional[str] = payload.get("sub")
        email: Optional[str] = payload.get("email")

        if email is None and username is None:
            raise HTTPException(status_code=401)

    except PyJWTError as jwt_error:
        logging.error(f"{datetime.datetime.utcnow()} | {jwt_error}")
        raise HTTPException(status_code=401)


async def provide_auth(login: str, password: str):
    user = await authenticate_user(login=login, password=password)

    if user is None:
        raise HTTPException(status_code=401)

    access_token = create_access_token(
        data={"sub": user["login"]},
    )

    return {"access_token": access_token, "token_type": "bearer"}


async def authenticate_user(login: str, password: str):
    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        user = await conn.fetchrow(  # language=PostgreSQL
            "SELECT * FROM users WHERE login = $1",
            login
        )
    await conn.close()

    if not dict(user):
        return None

    if verify_password(password, user["password_hash"]) is False:
        return None

    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            raise HTTPException(status_code=401)
        token_data = dict(login=login)
    except PyJWTError:
        raise HTTPException(status_code=401)

    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        user = await conn.fetchrow(  # language=PostgreSQL
            "SELECT * FROM users WHERE login = $1",
            token_data["login"]
        )
    await conn.close()

    if not dict(user):
        raise HTTPException(status_code=401)

    return user
