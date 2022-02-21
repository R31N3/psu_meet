from src.repo.base_enums import PydanticStringEnum


__all__ = ["Attendance"]


class Attendance(PydanticStringEnum):
    will_attend = "will_attend"
    attended = "attended"
    will_not_attend = "will_not_attend"
