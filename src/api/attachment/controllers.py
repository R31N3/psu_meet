from typing import Optional

import asyncpg
from fastapi import APIRouter, UploadFile, File, Depends, Form
from fastapi.responses import StreamingResponse
from uuid import uuid4, UUID

from src.api.attachment.enums import media_types_by_attachment_type, AttachmentType, AttachingEntityType
from src.api.users.service import get_current_user
from src.app import async_engine
from src.constants import DATA_DIR

attachments_router = APIRouter()

__all__ = [
    "attachments_router",
]


@attachments_router.post("/")
async def create_attachment(
        title: str = Form(...),
        description: Optional[str] = Form(...),
        attaching_entity_type: AttachingEntityType = Form(...),
        attaching_entity_id: UUID = Form(...),
        attachment_type: AttachmentType = Form(...),
        attachment_to_create: UploadFile = File(...),
        user=Depends(get_current_user)
):
    attachment_id = uuid4()
    attachment_path = DATA_DIR / f"{attachment_id}.{attachment_type.split('_')[0]}"
    with open(attachment_path, "wb+") as file:
        file.write(await attachment_to_create.read())

    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        result = await conn.fetchrow(  # language=PostgreSQL
            """
            INSERT INTO attachments 
            (
                id, author_id, title, description, attaching_entity_type, 
                attaching_entity_id, attachment_type, attachment_filepath
            )
            VALUES 
            ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING *
            """,
            uuid4(), user["id"], title, description, attaching_entity_type, attaching_entity_id,
            attachment_type, str(attachment_path)
        )
    await conn.close()

    return dict(result)


@attachments_router.get("/{attachment_id}/")
async def retrieve_attachment(attachment_id: UUID, _=Depends(get_current_user)):
    conn: asyncpg.Connection = (await async_engine.raw_connection()).connection._connection  # noqa
    async with conn.transaction():
        attachment = await conn.fetchrow(  # language=PostgreSQL
            "SELECT * FROM attachments WHERE id = $1", attachment_id
        )
    await conn.close()

    if attachment is not None:
        attachment_file = open(attachment["attachment_filepath"], "rb")
        return StreamingResponse(
            attachment_file, media_type=media_types_by_attachment_type[attachment["attachment_type"]]
        )
    else:
        return None


