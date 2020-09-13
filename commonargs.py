from typing import List, Optional, Type, Callable
from dataclasses import dataclass

import argparse
from pathlib import Path
import os


@dataclass
class Arguments:
    board_id: int

    db_file_path: Path
    base_log_folder_path: Path

    metadata_folder_path: Optional[Path]

    user_agent: str
    host: str
    appid: Optional[str]
    userhash: str

    def __str__(self) -> str:
        fields = dict(self.__dict__)
        fields["user_agent"] = "***已隐去***"
        fields["appid"] = "***已隐去***"
        fields["userhash"] = "***已隐去***"

        return f"{type(self).__name__}({fields})"


def parse_args(
    prog: str, args: List[str], description: str,
    args_cls: Type[Arguments], extra_args_fn: Optional[Callable[[argparse.ArgumentParser], None]] = None
) -> Arguments:

    parser = argparse.ArgumentParser(
        prog=prog,
        description=description,
    )

    parser.add_argument("-b", "--board-id",
                        help="采集目标版块的ID，默认为`111`", metavar="<board id like `111`>",
                        type=int, dest="board_id", default=111)
    parser.add_argument("--db", "--db-file",
                        help="用于存储采集数据的SQLite3数据库文件的路径", metavar="<path/to/db-file.sqlite3>",
                        type=Path, dest="db_file_path")
    parser.add_argument("--log-base-folder",
                        help="日志基目录的路径", metavar="<path/to/log-base-folder>",
                        type=Path, dest="base_log_folder_path")
    parser.add_argument("--metadata-folder",
                        help="元数据文件夹的路径，暂未被使用", metavar="<path/to/metadata-folder>",
                        type=Path, dest="metadata_folder_path", default=None)

    if extra_args_fn != None:
        extra_args_fn(parser)

    user_agent = os.environ["ADNMB_CLIENT_USER_AGENT"]
    host = os.environ["ADNMB_HOST"]
    appid = os.environ.get("ADNMB_CLIENT_APPID", None)
    userhash = os.environ["ADNMB_USERHASH"]

    args = parser.parse_args(args)

    return args_cls(
        **vars(args),

        user_agent=user_agent,
        host=host,
        appid=appid,
        userhash=userhash,
    )
