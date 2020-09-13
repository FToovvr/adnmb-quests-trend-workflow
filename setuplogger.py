import logging

from datetime import datetime
from pathlib import Path
import os

import pytz

tz = pytz.timezone("Asia/Shanghai")


class CustomLogFormatter(logging.Formatter):

    def formatTime(self, record: logging.LogRecord, datefmt: str = None):
        assert(datefmt == None)

        dt = datetime.fromtimestamp(record.created)
        dt = tz.localize(dt)

        return dt.isoformat(timespec="milliseconds")


def now_with_tz() -> pytz.datetime.datetime:
    return pytz.datetime.datetime.now(tz=tz)


def setup_logger(name: str, base_log_folder_path: Path) -> logging.Logger:
    pass

    logger = logging.getLogger(name)
    logger.level = logging.DEBUG

    formatter = CustomLogFormatter(
        '[%(asctime)s] @%(name)s #%(levelname)s: %(message)s',
    )

    consoleHandler = logging.StreamHandler()
    consoleHandler.level = logging.DEBUG
    consoleHandler.formatter = formatter

    log_folder_path = base_log_folder_path / name
    os.makedirs(log_folder_path, exist_ok=True)

    fileHandler = logging.FileHandler(
        filename=log_folder_path / now_with_tz().strftime("%Y-%m-%d_%H-%M%S.log"))
    fileHandler.level = logging.INFO
    fileHandler.formatter = formatter

    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    return logger
