import logging

from datetime import datetime, timezone
from pathlib import Path
import os


class CustomLogFormatter(logging.Formatter):

    def __init__(self, *args, tz: timezone, **kwargs):
        super(CustomLogFormatter, self).__init__(*args, **kwargs)
        self.time_zone = tz

    def formatTime(self, record: logging.LogRecord, datefmt: str = None):
        assert(datefmt == None)

        dt = datetime.fromtimestamp(record.created, tz=self.time_zone)

        return dt.isoformat(timespec="milliseconds")


__has_setup_root_logger = False
__base_log_folder_path = None


def __setup_aqt_root_logger(base_log_folder_path: Path, tz: timezone):
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
        tz=tz,
    )

    consoleHandler = logging.StreamHandler()
    consoleHandler.level = logging.DEBUG
    consoleHandler.formatter = formatter

    os.makedirs(base_log_folder_path, exist_ok=True)

    fileHandler = logging.FileHandler(
        filename=base_log_folder_path / datetime.now(tz=tz).strftime("%Y-%m-%d_%H-%M%S.log"))
    fileHandler.level = logging.INFO
    fileHandler.formatter = formatter

    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)


def setup_aqt_logger(name: str, base_log_folder_path: Path, tz: timezone) -> logging.Logger:
    # AQT = adnmb_quests_trend

    __setup_aqt_root_logger(base_log_folder_path, tz)

    return logging.getLogger(f"AQT.{name}")
