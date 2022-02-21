from typing import Callable

from fastapi import FastAPI
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from src.utils.json_tools import orjson_loads, orjson_dumps

__all__ = [
    "app",
    "async_engine",
    "LocalSession",
    "DB",
]


app: FastAPI = FastAPI(title="Just Study", debug=True)


async_engine = create_async_engine(
    URL.create(
        drivername="postgresql+asyncpg",
        username="postgres",
        password="qwerty",
        database="scratch",
        host="localhost",
        port="5432",
    ),
    json_deserializer=orjson_loads,
    json_serializer=orjson_dumps,
    echo=True,
)

LocalSession: Callable[[], AsyncSession] = sessionmaker(
    bind=async_engine, class_=AsyncSession, autoflush=True, expire_on_commit=False
)

DB = declarative_base(bind=async_engine)
