from uuid import UUID

from pydantic import BaseModel

from src.api.attachment.enums import AttachingEntityType, AttachmentType

__all__ = ["CreateAttachmentFAPI"]


class CreateAttachmentFAPI(BaseModel):
    attaching_entity_type: AttachingEntityType
    attaching_entity_id: UUID
    attachment_type: AttachmentType
