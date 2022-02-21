import pathlib

from src.utils.configuration import init_config

__all__ = [
    "PROJECT_DIR",
    "DATA_DIR",
    "CONFIG",
]

from src.utils.extra_utils import make_dir_if_not_exists

CONFIG = init_config()
PROJECT_DIR = pathlib.Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "data"

make_dir_if_not_exists(str(DATA_DIR))
