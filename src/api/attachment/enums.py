from typing import Dict

from src.repo.base_enums import PydanticStringEnum


__all__ = ["AttachingEntityType", "AttachmentType"]


class AttachingEntityType(PydanticStringEnum):
    user = "user"
    subject_schedule = "subject_schedule"
    task = "task"
    user_task = "user_task"


class AttachmentType(PydanticStringEnum):
    png_image = "png_image"
    jpg_image = "jpg_image"
    docx_document = "docx_document"
    xlsx_document = "xlsx_document"
    pptx_document = "pptx_document"
    vsdx_document = "vsdx_document"
    pdf_document = "pdf_document"
    zip_archive = "zip_archive"


media_types_by_attachment_type: Dict[AttachmentType, str] = {
    AttachmentType.png_image: "image/png",
    AttachmentType.jpg_image: "image/jpg",
    AttachmentType.docx_document: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    AttachmentType.xlsx_document: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    AttachmentType.pptx_document: "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    AttachmentType.vsdx_document: "application/vnd.visio2013",
    AttachmentType.pdf_document: "application/pdf",
    AttachmentType.zip_archive: "application/zip",
}
