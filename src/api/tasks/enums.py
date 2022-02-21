from src.repo.base_enums import PydanticStringEnum


__all__ = ["TaskType", "TaskDateType"]


class TaskType(PydanticStringEnum):
    lab = "lab"
    essay = "essay"
    test = "test"
    exam = "exam"


class TaskDateType(PydanticStringEnum):
    until_date = "until_date"
    date = "date"
    limitless = "limitless"


class AttemptStatus(PydanticStringEnum):
    pending = "pending"
    approved = "approved"
    denied = "denied"
