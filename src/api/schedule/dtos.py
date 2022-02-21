import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator

from src.api.schedule.enums import ConferenceType
from src.repo.base_validators import datetime_validator

__all__ = ["CreateScheduleFAPI"]


class CreateScheduleFAPI(BaseModel):
    subject_id: UUID
    teacher_id: Optional[UUID]
    students_group_id: UUID

    scheduled_start: datetime.datetime
    scheduled_stop: datetime.datetime

    conference_type: Optional[ConferenceType]
    conference_url: Optional[str]

    is_replacement: Optional[bool] = False

    @validator("scheduled_start", "scheduled_stop", pre=True, always=True)
    def validate_schedule(cls, var):  # noqa
        return datetime_validator(var)
