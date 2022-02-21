import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator

from src.repo.base_validators import datetime_validator
from src.api.attendance.enums import Attendance

__all__ = ["CreateAttendanceFAPI"]


class CreateAttendanceFAPI(BaseModel):
    schedule_id: UUID

    attendance: Optional[Attendance] = Attendance.attended
    attendance_start: datetime.datetime
    attendance_stop: datetime.datetime

    @validator("attendance_start", "attendance_stop", pre=True, always=True)
    def validate_schedule(cls, var):  # noqa
        return datetime_validator(var)
