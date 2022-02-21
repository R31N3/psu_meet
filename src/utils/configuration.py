import argparse
import os
import pathlib
from typing import Any, Optional, List

import trafaret
from trafaret_config import commandline

__all__ = ["get_config", "init_config"]


PATH = pathlib.Path(__file__).parent.parent.parent
settings_file = os.environ.get("SETTINGS_FILE", "api.dev.yml")
DEFAULT_CONFIG_PATH = PATH / "config" / settings_file


CONFIG_TRAFARET = trafaret.Dict(
    {
        trafaret.Key("app"): trafaret.Dict(
            {
                "backend": trafaret.Dict(
                    {
                        "host": trafaret.String(),
                        "port": trafaret.Int(),
                    }
                ),
            }
        ),
    }
)


def get_config(argv: Any = None) -> Any:
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        ap,
        default_config=DEFAULT_CONFIG_PATH,
    )

    # ignore unknown options
    options, unknown = ap.parse_known_args(argv)

    config = commandline.config_from_options(options, CONFIG_TRAFARET)

    return config


def init_config(*, config: Optional[List[str]] = None):
    return get_config(config or ["-c", DEFAULT_CONFIG_PATH.as_posix()])
