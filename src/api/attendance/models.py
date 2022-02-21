from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Boolean, Enum, String
from sqlalchemy.dialects.postgresql import UUID

from src.api.attendance.enums import Attendance
from src.app import DB
from src.repo.base_models import BaseDateTimeModel
from src.repo.sa_types import SqlalchemyTypesMixin

__all__ = [
    "AttendanceORM",
]


class AttendanceORM(DB, SqlalchemyTypesMixin, BaseDateTimeModel):
    __tablename__ = "scheduled_subjects_attendances"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    schedule_id = Column(UUID(as_uuid=True), nullable=False)

    attendance = Column(Enum(Attendance), nullable=False, default=Attendance.will_attend,)
    attendance_start = Column(DateTime, nullable=False,)
    attendance_stop = Column(DateTime, nullable=False,)

    is_confirmed = Column(Boolean, nullable=True, default=None)

    __table_args__ = (
        ForeignKeyConstraint(("user_id",), ["users.id"], ondelete="RESTRICT", name="__user_id_fk"),
        ForeignKeyConstraint(
            ("schedule_id",), ["subjects_schedules.id"], ondelete="RESTRICT", name="__schedule_id_fk"
        ),
    )
