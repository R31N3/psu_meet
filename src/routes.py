from fastapi.responses import ORJSONResponse

from src.api.users.controllers import users_router
from src.api.tasks.controllers import tasks_router
from src.api.subjects.controllers import subjects_router
from src.api.schedule.controllers import schedule_router
from src.api.attendance.controllers import attendance_router
from src.api.attachment.controllers import attachments_router


__all__ = ["init_routes"]


def init_routes(app):
    include_route = app.router.include_router

    include_route(
        users_router,
        default_response_class=ORJSONResponse,
        tags=["Users"],
        prefix="/api/users",
    )

    include_route(
        attachments_router,
        default_response_class=ORJSONResponse,
        tags=["Attachments"],
        prefix="/api/attachments",
    )

    include_route(
        subjects_router,
        default_response_class=ORJSONResponse,
        tags=["Subjects"],
        prefix="/api/subjects",
    )

    include_route(
        schedule_router,
        default_response_class=ORJSONResponse,
        tags=["Schedule"],
        prefix="/api/schedule",
    )

    include_route(
        attendance_router,
        default_response_class=ORJSONResponse,
        tags=["Attendance"],
        prefix="/api/attendance",
    )

    include_route(
        tasks_router,
        default_response_class=ORJSONResponse,
        tags=["Tasks"],
        prefix="/api/tasks",
    )
