import datetime
import logging
import time

from asyncpg.exceptions import CannotConnectNowError, DuplicateTableError, UniqueViolationError, DuplicateObjectError

from src.app import DB, async_engine

__all__ = [
    "setup_tables_before_start",
]


async def setup_tables_before_start():
    timeout = 3
    max_attempts = 10

    for i in range(max_attempts):

        try:
            logging.critical(f"{datetime.datetime.utcnow()} | Trying to create tables, attempt {i + 1}...")

            async with async_engine.begin() as conn:
                await conn.run_sync(DB.metadata.create_all)

        except CannotConnectNowError:
            logging.critical(f"{datetime.datetime.utcnow()} | failed. Waiting for retry with timeout={timeout}s")
            time.sleep(timeout)

        except (DuplicateTableError, UniqueViolationError, DuplicateObjectError, ConnectionRefusedError) as exc:
            logging.critical(exc)
            pass
