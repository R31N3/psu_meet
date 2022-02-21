import os


__all__ = [
    "make_dir_if_not_exists",
]


def make_dir_if_not_exists(directory_name: str):
    try:
        os.mkdir(directory_name)
    except FileExistsError:
        pass
