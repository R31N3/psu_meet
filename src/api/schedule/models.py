from sqlalchemy import Column, DateTime, Enum, ForeignKeyConstraint, Boolean, String
from sqlalchemy.dialects.postgresql import UUID

from src.api.schedule.enums import ConferenceType
from src.app import DB
from src.repo.base_models import BaseDateTimeModel
from src.repo.sa_types import SqlalchemyTypesMixin

__all__ = [
    "ScheduleORM",
]


class ScheduleORM(DB, SqlalchemyTypesMixin, BaseDateTimeModel):
    __tablename__ = "subjects_schedules"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    author_id = Column(UUID(as_uuid=True), nullable=False)
    subject_id = Column(UUID(as_uuid=True), nullable=False)
    teacher_id = Column(UUID(as_uuid=True), nullable=False)
    students_group_id = Column(UUID(as_uuid=True), nullable=False)

    scheduled_start = Column(DateTime, nullable=False,)
    scheduled_stop = Column(DateTime, nullable=False,)

    conference_type = Column(Enum(ConferenceType), nullable=True)
    conference_url = Column(String, nullable=True)

    is_replacement = Column(Boolean, nullable=False, default=False)

    __table_args__ = (
        ForeignKeyConstraint(("author_id",), ["users.id"], ondelete="RESTRICT", name="__author_id_fk"),
        ForeignKeyConstraint(
            ("subject_id",), ["subjects.id"], ondelete="RESTRICT", name="__subject_id_fk"
        ),
        ForeignKeyConstraint(
            ("teacher_id",), ["users.id"], ondelete="RESTRICT", name="__teacher_id_fk"
        ),
        ForeignKeyConstraint(
            ("students_group_id",), ["users_groups.id"], ondelete="RESTRICT", name="__students_group_id_fk"
        ),
    )
