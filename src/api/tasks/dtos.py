import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, validator

from src.repo.base_validators import datetime_validator
from src.api.tasks.enums import TaskDateType

__all__ = ["CreateTaskFAPI", "CreateTaskAttemptFAPI"]


class CreateTaskFAPI(BaseModel):
    teacher_id: UUID
    subject_id: UUID
    students_groups_ids: List[UUID]

    title: str
    description: str

    date: Optional[datetime.datetime]
    date_type: TaskDateType
    possible_score: Optional[int] = 1
    attempts_limit: Optional[int]

    @validator("date", pre=True, always=True)
    def validate_date(cls, var):  # noqa
        return datetime_validator(var)


class CreateTaskAttemptFAPI(BaseModel):
    task_id: UUID
    attachment_id: Optional[UUID]

    description: Optional[str]
