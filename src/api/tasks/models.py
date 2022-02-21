from sqlalchemy import Column, String, Boolean, ForeignKeyConstraint, DateTime, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID

from src.api.tasks.enums import TaskDateType, AttemptStatus
from src.app import DB
from src.repo.base_models import BaseDateTimeModel
from src.repo.sa_types import SqlalchemyTypesMixin

__all__ = [
    "TaskORM", "UserTaskAttemptORM"
]


class TaskORM(DB, SqlalchemyTypesMixin, BaseDateTimeModel):
    __tablename__ = "subjects_tasks"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    author_id = Column(UUID(), nullable=False)
    teacher_id = Column(UUID(), nullable=False)
    subject_id = Column(UUID(), nullable=False)
    students_group_id = Column(UUID(as_uuid=True), nullable=False)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    date = Column(DateTime, nullable=True,)
    date_type = Column(Enum(TaskDateType), nullable=False)
    possible_score = Column(Integer, nullable=False, default=1)
    attempts_limit = Column(Integer, nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(("author_id",), ["users.id"], ondelete="RESTRICT", name="__author_id_fk"),
        ForeignKeyConstraint(("teacher_id",), ["users.id"], ondelete="RESTRICT", name="__teacher_id_fk"),
        ForeignKeyConstraint(("subject_id",), ["subjects.id"], ondelete="RESTRICT", name="__subject_id_fk"),
        ForeignKeyConstraint(
            ("students_group_id",), ["users_groups.id"], ondelete="RESTRICT", name="__students_group_id_fk"
        ),
    )


class UserTaskAttemptORM(DB, SqlalchemyTypesMixin, BaseDateTimeModel):
    __tablename__ = "users_tasks_attempts"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    author_id = Column(UUID(), nullable=False)
    task_id = Column(UUID(), nullable=False)
    attachment_id = Column(UUID(as_uuid=True), nullable=True)

    description = Column(String, nullable=True)
    attempt_status = Column(Enum(AttemptStatus), nullable=True, default=AttemptStatus.pending)
    score = Column(Integer, nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(("author_id",), ["users.id"], ondelete="RESTRICT", name="__author_id_fk"),
        ForeignKeyConstraint(("task_id",), ["subjects_tasks.id"], ondelete="RESTRICT", name="__task_id_fk"),
        ForeignKeyConstraint(
            ("attachment_id",), ["attachments.id"], ondelete="SET NULL", name="__attachment_id_fk"
        ),
    )

