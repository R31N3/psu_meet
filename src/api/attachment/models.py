from sqlalchemy import Column, ForeignKeyConstraint, Enum, String
from sqlalchemy.dialects.postgresql import UUID

from src.api.attachment.enums import AttachingEntityType, AttachmentType
from src.app import DB
from src.repo.base_models import BaseDateTimeModel
from src.repo.sa_types import SqlalchemyTypesMixin

__all__ = [
    "AttachmentORM",
]


class AttachmentORM(DB, SqlalchemyTypesMixin, BaseDateTimeModel):
    __tablename__ = "attachments"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    author_id = Column(UUID(as_uuid=True), nullable=False,)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    attaching_entity_type = Column(Enum(AttachingEntityType), nullable=False,)
    attaching_entity_id = Column(UUID(as_uuid=True), nullable=False,)
    attachment_type = Column(Enum(AttachmentType), nullable=False,)
    attachment_filepath = Column(String, nullable=False,)

    __table_args__ = (
        ForeignKeyConstraint(("author_id",), ["users.id"], ondelete="RESTRICT", name="__author_id_fk"),
    )
