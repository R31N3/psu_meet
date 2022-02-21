from src.repo.base_enums import PydanticStringEnum


__all__ = ["UserRole", "UserState"]


class UserRole(PydanticStringEnum):
    administrator = "administrator"
    teacher = "teacher"
    student = "student"


class UserState(PydanticStringEnum):
    active = "active"
    deactivated = "deactivated"
    archive = "archive"
