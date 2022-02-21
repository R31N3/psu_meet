from typing import Optional
from uuid import UUID

from pydantic import BaseModel

__all__ = ["CreateSubjectFAPI"]


class CreateSubjectFAPI(BaseModel):
    default_teacher_id: UUID

    title: str
    description: Optional[str]
