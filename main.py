import os

import uvicorn

from src.app import app as initial_app
from src.constants import CONFIG
from src.init_app import init_app

app = init_app(initial_app)


if __name__ == "__main__":
    # noinspection PyTypeChecker
    uvicorn.run(app, **CONFIG["app"]["backend"], debug=os.environ.get("DEBUG", True), log_level="debug")
