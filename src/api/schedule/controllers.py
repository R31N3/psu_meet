import datetime
from typing import Optional

import asyncpg
from fastapi import APIRouter
from fastapi import Depends
from uuid import uuid4

from src.api.schedule.dtos import CreateScheduleFAPI
from src.api.users.service import get_current_user
from src.app import async_engine

schedule_router = APIRouter()

__all__ = [
    "schedule_router",
]


@schedule_router.post("/")
async def create_schedule(schedule_to_create: CreateScheduleFAPI, user=Depends(get_current_user)):
    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        schedule_to_create.teacher_id = (
            schedule_to_create.teacher_id
            or dict(await conn.fetchrow(  # language=PostgreSQL
                """SELECT default_teacher_id FROM subjects WHERE id = $1""",
                schedule_to_create.subject_id
            ))["default_teacher_id"]
        )

        result = await conn.fetchrow(  # language=PostgreSQL
            """
            INSERT INTO subjects_schedules 
            (
                id, author_id, subject_id, teacher_id, students_group_id, scheduled_start, scheduled_stop,
                conference_type, conference_url, is_replacement
            )
            VALUES 
            ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            RETURNING *
            """,
            uuid4(), user["id"], *list(schedule_to_create.dict().values())
        )
    await conn.close()

    return dict(result)


@schedule_router.get("/teacher")
async def retrieve_teacher_schedule(
        week_start_day: datetime.date, week_end_day: Optional[datetime.date], teacher=Depends(get_current_user)
):
    week_end_day = week_end_day or week_start_day + datetime.timedelta(days=6)
    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        student_schedule = await conn.fetch(  # language=PostgreSQL
            """
            SELECT schedules.*, 
             subjects as subject,
             (
                SELECT CONCAT(users.lastname, ' ', users.firstname, ' ', users.surname) 
                FROM users WHERE users.id = schedules.teacher_id
             ) as teacher
            FROM subjects_schedules as schedules
            INNER JOIN subjects on subjects.id = schedules.subject_id
            WHERE schedules.teacher_id = $1 AND CAST(schedules.scheduled_start as date) >= $2 
            AND CAST(schedules.scheduled_stop as date) <= $3 
            """,
            teacher["id"], week_start_day, week_end_day
        )
    await conn.close()

    return sorted([dict(schedule) for schedule in student_schedule], key=lambda x: x["scheduled_start"])


@schedule_router.get("/student")
async def retrieve_student_schedule(
        week_start_day: datetime.date, week_end_day: Optional[datetime.date], student=Depends(get_current_user)
):
    week_end_day = week_end_day or week_start_day + datetime.timedelta(days=6)
    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        student_schedule = await conn.fetch(  # language=PostgreSQL
            """
            SELECT schedules.*, 
             subjects as subject,
             (
                SELECT CONCAT(users.lastname, ' ', users.firstname, ' ', users.surname) 
                FROM users WHERE users.id = schedules.teacher_id
             ) as teacher,
             (ssa.attendance, ssa.attendance_start, ssa.attendance_stop) as attendance
            FROM subjects_schedules as schedules
            INNER JOIN subjects on subjects.id = schedules.subject_id
            LEFT JOIN scheduled_subjects_attendances as ssa on schedules.id = ssa.schedule_id AND ssa.user_id = $1
            WHERE (
                SELECT ugr.user_id 
                FROM users_groups_relations as ugr WHERE ugr.user_group_id = schedules.students_group_id AND ugr.user_id = $1
            ) = $1 AND CAST(schedules.scheduled_start as date) >= $2 
            AND CAST(schedules.scheduled_stop as date) <= $3 
            """,
            student["id"], week_start_day, week_end_day
        )
    await conn.close()

    return sorted([dict(schedule) for schedule in student_schedule], key=lambda x: x["scheduled_start"])
