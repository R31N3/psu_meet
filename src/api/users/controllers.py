import asyncpg
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from uuid import uuid4

from src.api.users.dtos import CreateUserFAPI, CreateUserGroupFAPI
from src.api.users.service import provide_auth, get_current_user
from src.app import async_engine

users_router = APIRouter()

__all__ = [
    "users_router",
]


@users_router.post("/")
async def register_user(user_to_create: CreateUserFAPI, _=Depends(get_current_user)):
    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        result = await conn.fetchrow(  # language=PostgreSQL
            """
            INSERT INTO users 
            (id, login, email, firstname, lastname, surname, role, password_hash, expire_date) 
            VALUES 
            ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING *
            """,
            uuid4(), *list(user_to_create.dict().values())
        )
    await conn.close()

    return dict(result)


@users_router.post("/auth")
async def auth_user(form_data: OAuth2PasswordRequestForm = Depends()):
    return await provide_auth(login=form_data.username, password=form_data.password)


@users_router.post("/users_group")
async def create_user_group(user_group_to_create: CreateUserGroupFAPI, user=Depends(get_current_user)):
    user_group_to_create.curator_id = user_group_to_create.curator_id or user["id"]
    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        created_group = await conn.fetchrow(  # language=PostgreSQL
            """
            INSERT INTO users_groups
            (id, author_id, curator_id, title, description)
            VALUES 
            ($1, $2, $3, $4, $5)
            RETURNING *
            """,
            uuid4(), user["id"], *(list(user_group_to_create.dict().values())[:-1])
        )
        for user_id, is_head_of_group in user_group_to_create.group_users_info:
            await conn.fetchrow(  # language=PostgreSQL
                """
                INSERT INTO users_groups_relations
                (id, user_id, is_head_of_group)
                VALUES
                ($1, $2, $3)
                """,
                uuid4(), user_id, is_head_of_group
            )
    await conn.close()

    return dict(created_group)
