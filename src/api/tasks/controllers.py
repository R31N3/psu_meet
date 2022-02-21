import asyncpg
from fastapi import APIRouter
from fastapi import Depends
from uuid import uuid4, UUID

from src.api.tasks.dtos import CreateTaskFAPI, CreateTaskAttemptFAPI
from src.api.users.service import get_current_user
from src.app import async_engine

tasks_router = APIRouter()

__all__ = [
    "tasks_router",
]


@tasks_router.post("/")
async def create_task(task_to_create: CreateTaskFAPI, user=Depends(get_current_user)):
    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        for user_group_id in task_to_create.students_groups_ids:
            result = await conn.fetchrow(  # language=PostgreSQL
                """
                INSERT INTO subjects_tasks 
                (
                    id, author_id, teacher_id, subject_id, students_group_id, title,
                     description, date, date_type, possible_score, attempts_limit
                )
                VALUES 
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                RETURNING *
                """,
                uuid4(),
                user["id"],
                task_to_create.teacher_id,
                task_to_create.subject_id,
                user_group_id,
                *(list(task_to_create.dict().values())[3:])
            )
    await conn.close()

    return dict(result)


@tasks_router.post("/attempt")
async def create_task_attempt(attempt_to_create: CreateTaskAttemptFAPI, user=Depends(get_current_user)):
    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        result = await conn.fetchrow(  # language=PostgreSQL
            """
            INSERT INTO users_tasks_attempts 
            (id, author_id, task_id, attachment_id, description)
            VALUES 
            ($1, $2, $3, $4, $5)
            RETURNING *
            """,
            uuid4(), user["id"], *list(attempt_to_create.dict().values())
        )
    await conn.close()

    return dict(result)


@tasks_router.get("/student")
async def get_tasks_by_subject_student(subject_id: UUID, student=Depends(get_current_user)):
    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        user_tasks_by_ids = {
            task["id"]: dict(task)
            for task in await conn.fetch(  # language=PostgreSQL
                """
                SELECT subjects_tasks.*
                FROM subjects_tasks 
                WHERE (
                    SELECT ugr.user_id 
                    FROM users_groups_relations as ugr
                    WHERE ugr.user_group_id = subjects_tasks.students_group_id AND ugr.user_id = $1
                ) = $1 AND subjects_tasks.subject_id = $2
                """,
                student["id"], subject_id
            )
        }
        for task_attempt in await conn.fetch(  # language=PostgreSQL
            "SELECT * FROM users_tasks_attempts WHERE author_id = $1 AND task_id = any($2::uuid[])",
            student["id"], list(user_tasks_by_ids.keys())
        ):
            user_tasks_by_ids[task_attempt["task_id"]]["attempts"] = (
                    user_tasks_by_ids.get("attempts", []) + [task_attempt]
            )

        for task_attachment in await conn.fetch(  # language=PostgreSQL
            "SELECT * FROM attachments WHERE attaching_entity_type = 'task' and attaching_entity_id = any($1::uuid[])",
            list(user_tasks_by_ids.keys())
        ):
            user_tasks_by_ids[task_attachment["attaching_entity_id"]]["task_attachments"] = (
                user_tasks_by_ids[task_attachment["attaching_entity_id"]].get("attachments", []) + [task_attachment]
            )

        for task in user_tasks_by_ids.values():
            for attempts_attachments in await conn.fetch(  # language=PostgreSQL
                """
                SELECT *
                 FROM attachments 
                 WHERE attaching_entity_type = 'user_task' and attaching_entity_id = any($1::uuid[])
                 """,
                list(attempt["id"] for attempt in task.get("attempts", []))
            ):
                user_tasks_by_ids[task["id"]]["task_attachments"] = (
                    user_tasks_by_ids[task["id"]].get("attachments", []) + [attempts_attachments]
                )

    await conn.close()

    return user_tasks_by_ids


@tasks_router.get("/teacher")
async def get_task_by_subject_teacher(subject_id: UUID, _=Depends(get_current_user)):
    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        subject_tasks_by_ids = {
            task["id"]: {**dict(task), **dict(attempts_by_users={})}
            for task in await conn.fetch(  # language=PostgreSQL
                "SELECT subjects_tasks.* FROM subjects_tasks WHERE subjects_tasks.subject_id = $1", subject_id
            )
        }

        for task_attempt in await conn.fetch(  # language=PostgreSQL
            "SELECT * FROM users_tasks_attempts WHERE task_id = any($1::uuid[])", list(subject_tasks_by_ids.keys())
        ):
            task_id = task_attempt["task_id"]
            subject_tasks_by_ids[task_id]["attempts_by_users"][task_attempt["author_id"]] = (
                subject_tasks_by_ids[task_id]["attempts_by_users"].get(task_attempt["author_id"], []) + [task_attempt]
            )

        for task_attachment in await conn.fetch(  # language=PostgreSQL
            "SELECT * FROM attachments WHERE attaching_entity_type = 'task' and attaching_entity_id = any($1::uuid[])",
            list(subject_tasks_by_ids.keys())
        ):
            subject_tasks_by_ids[task_attachment["attaching_entity_id"]]["attachments"] = (
                subject_tasks_by_ids[task_attachment["attaching_entity_id"]].get("attachments", []) + [task_attachment]
            )

        for task in subject_tasks_by_ids.values():
            for attempts_attachments in await conn.fetch(  # language=PostgreSQL
                """
                SELECT *
                 FROM attachments 
                 WHERE attaching_entity_type = 'user_task' and attaching_entity_id = any($1::uuid[])
                 """,
                list(
                    attempt["id"]
                    for user_attempts in task.get("attempts_by_users", {}).values()
                    for attempt in user_attempts
                )
            ):
                subject_tasks_by_ids[task["id"]]["attachments"] = (
                    subject_tasks_by_ids[task["id"]].get("attachments", []) + [attempts_attachments]
                )

    await conn.close()

    return subject_tasks_by_ids
