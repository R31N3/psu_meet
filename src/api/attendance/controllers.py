import asyncpg
from fastapi import APIRouter
from fastapi import Depends
from uuid import uuid4,UUID

from src.api.attendance.dtos import CreateAttendanceFAPI
from src.api.users.service import get_current_user
from src.app import async_engine

attendance_router = APIRouter()

__all__ = [
    "attendance_router",
]


@attendance_router.post("/")
async def create_attendance(attendance_to_create: CreateAttendanceFAPI, user=Depends(get_current_user)):
    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        result = await conn.fetchrow(  # language=PostgreSQL
            """
            INSERT INTO scheduled_subjects_attendances 
            (id, user_id, schedule_id, attendance, attendance_start, attendance_stop)
            VALUES 
            ($1, $2, $3, $4, $5, $6)
            RETURNING *
            """,
            uuid4(), user["id"], *list(attendance_to_create.dict().values())
        )
    await conn.close()

    return dict(result)


@attendance_router.get("/student")
async def get_attendance_by_schedule_student(schedule_id: UUID, student=Depends(get_current_user)):
    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        student_attendances = await conn.fetch(  # language=PostgreSQL
            """
            SELECT * FROM scheduled_subjects_attendances WHERE user_id = $1 AND schedule_id = $2
            """,
            student["id"], schedule_id
        )
    await conn.close()

    return [dict(attend) for attend in student_attendances]


@attendance_router.get("/teacher")
async def get_attendance_by_schedule_teacher(schedule_id: UUID, _=Depends(get_current_user)):
    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        students_attendances = await conn.fetch(  # language=PostgreSQL
            """
            SELECT *, (
                SELECT CONCAT(users.lastname, ' ', users.firstname, ' ', users.surname) as user_info
                 FROM users 
                 WHERE users.id = scheduled_subjects_attendances.user_id
             )
             FROM scheduled_subjects_attendances WHERE schedule_id = $1
            """,
            schedule_id,
        )
    await conn.close()

    return [dict(attend) for attend in students_attendances]
