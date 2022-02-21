import asyncpg
from fastapi import APIRouter
from fastapi import Depends
from uuid import uuid4

from src.api.subjects.dtos import CreateSubjectFAPI
from src.api.users.service import get_current_user
from src.app import async_engine

subjects_router = APIRouter()

__all__ = [
    "subjects_router",
]


@subjects_router.post("/")
async def create_subject(subject_to_create: CreateSubjectFAPI, user=Depends(get_current_user)):
    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        result = await conn.fetchrow(  # language=PostgreSQL
            """
            INSERT INTO subjects 
            (id, author_id, default_teacher_id, title, description)
            VALUES 
            ($1, $2, $3, $4, $5)
            RETURNING *
            """,
            uuid4(), user["id"], *list(subject_to_create.dict().values())
        )
    await conn.close()

    return dict(result)
