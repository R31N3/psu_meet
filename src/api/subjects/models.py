from sqlalchemy import Column, String, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID

from src.app import DB
from src.repo.base_models import BaseDateTimeModel
from src.repo.sa_types import SqlalchemyTypesMixin

__all__ = [
    "SubjectORM",
]


class SubjectORM(DB, SqlalchemyTypesMixin, BaseDateTimeModel):
    __tablename__ = "subjects"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    author_id = Column(UUID(), nullable=False)
    default_teacher_id = Column(UUID(), nullable=False)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(("author_id",), ["users.id"], ondelete="RESTRICT", name="__author_id_fk"),
        ForeignKeyConstraint(
            ("default_teacher_id",), ["users.id"], ondelete="RESTRICT", name="__default_teacher_id_fk"
        ),
    )
