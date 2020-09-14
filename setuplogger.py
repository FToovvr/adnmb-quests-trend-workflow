import logging

from datetime import datetime
from pathlib import Path
import os

from dateutil import tz

local_tz = tz.gettz("Asia/Shanghai")


class CustomLogFormatter(logging.Formatter):

    def formatTime(self, record: logging.LogRecord, datefmt: str = None):
        assert(datefmt == None)

        dt = datetime.fromtimestamp(record.created, tz=local_tz)

        return dt.isoformat(timespec="milliseconds")


def now_with_tz() -> datetime:
    return datetime.now(tz=local_tz)


__has_setup_root_logger = False
__base_log_folder_path = None


def __setup_aqt_root_logger(base_log_folder_path: Path):
    global __has_setup_root_logger, __base_log_folder_path
    if __has_setup_root_logger:
        assert(__base_log_folder_path == base_log_folder_path)
        return
    else:
        __has_setup_root_logger = True
        __base_log_folder_path = base_log_folder_path

    logger = logging.getLogger("AQT")
    logger.level = logging.DEBUG

    formatter = CustomLogFormatter(
        '[%(asctime)s] @%(name)s #%(levelname)s: %(message)s',
    )

    consoleHandler = logging.StreamHandler()
    consoleHandler.level = logging.DEBUG
    consoleHandler.formatter = formatter

    os.makedirs(base_log_folder_path, exist_ok=True)

    fileHandler = logging.FileHandler(
        filename=base_log_folder_path / now_with_tz().strftime("%Y-%m-%d_%H-%M%S.log"))
    fileHandler.level = logging.INFO
    fileHandler.formatter = formatter

    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)


def setup_aqt_logger(name: str, base_log_folder_path: Path) -> logging.Logger:
    # AQT = adnmb_quests_trend

    __setup_aqt_root_logger(base_log_folder_path)

    return logging.getLogger(f"AQT.{name}")
