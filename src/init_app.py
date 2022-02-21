from fastapi import FastAPI

from src.repo.setup_before_start import setup_tables_before_start
from src.routes import init_routes

__all__ = [
    "init_app",
]


def init_app(app: FastAPI) -> FastAPI:
    init_routes(app)

    app.add_event_handler("startup", setup_tables_before_start)

    return app
