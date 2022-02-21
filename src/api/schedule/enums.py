from src.repo.base_enums import PydanticStringEnum


__all__ = ["ConferenceType"]


class ConferenceType(PydanticStringEnum):
    skype = "skype"
    zoom = "zoom"
    google_meet = "google_meet"
    jitsi = "jitsi"
