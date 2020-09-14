#!/usr/bin/env python3
from typing import List, Union, Literal, Optional, Tuple
from dataclasses import dataclass
from contextlib import contextmanager

import argparse
import sys
import logging

import anobbsclient

from commonargs import parse_args, Arguments
from setuplogger import setup_aqt_logger

import collect_posts
from exceptions import QuitDueToTrendThreadRelatedIssueException


@dataclass
class RunWorkflowArguments(Arguments):
    range: Union[Literal["yesterday"], Literal["last-24-hours"]]

    trend_thread_id: Optional[int]

    @staticmethod
    def _parse_extra_args(parser: argparse.ArgumentParser):
        parser.add_argument("-r", "--range",
                            choices=["yesterday", "last-24-hours"],
                            help="统计模式。" +
                            "若为 `yesterday`，将以流程开始时的前一整天作为统计范围；" +
                            "若为 `last-24-hours`，将以流程开始起向前24小时作为统计范围。",
                            dest="range")
        parser.add_argument("--trend-thread-id",
                            help="趋势串的串号", metavar="<trend thread id>",
                            type=int, dest="trend_thread_id", default=None)


@dataclass
class StepManager:
    logger: logging.Logger
    n: int = 0

    @contextmanager
    def next(self, name: str):
        self.n += 1
        self.logger.info(f"{self.n}. {name}：开始")
        try:
            yield (self.n, name)
        except Exception as e:
            self.logger.info(f"{self.n}. {name}：遭遇异常，流程将中断", exc_info=e)
            exit(1)
        self.logger.info(f"{self.n}. {name}：完成")


def main(args: List[str]):
    args: RunWorkflowArguments = parse_args(
        prog=args[0],
        args=args[1:],
        description="运行跑团版趋势工作流程",
        args_cls=RunWorkflowArguments,
        extra_args_fn=RunWorkflowArguments._parse_extra_args)

    logger = setup_aqt_logger(
        name="workflow",  # AQT = adnmb_quests_trend
        base_log_folder_path=args.base_log_folder_path,
        tz=args.time_zone,
    )

    logger.info(f"输入参数：{args}")

    client = anobbsclient.Client(
        user_agent=args.user_agent,
        host=args.host,
        appid=args.appid,
        default_request_options={
            "user_cookie": anobbsclient.UserCookie(
                userhash=args.userhash,
            ),
        },
    )

    logger.info(f"跑团版趋势工作流程：开始")
    sm = StepManager(logger)

    with sm.next("检查趋势串"):
        if args.trend_thread_id != None:
            (can_continue, quit_reason) = check_trend_thread(
                client, args.trend_thread_id)
            if not can_continue:
                raise QuitDueToTrendThreadRelatedIssueException(quit_reason)
        else:
            logger.info(f"未配置趋势串，跳过")

    with sm.next("采集跑团版"):
        collect_posts.execute(collect_posts.CollectArguments(
            board_id=args.board_id,
            db_file_path=args.db_file_path,
            base_log_folder_path=args.base_log_folder_path,
            metadata_folder_path=args.metadata_folder_path,
            user_agent=args.user_agent,
            host=args.host,
            appid=args.appid,
            userhash=args.userhash,
            time_zone=args.time_zone,
        ), client)

    logger.info(f"跑团版趋势工作流程：完成")


def check_trend_thread(client: anobbsclient.Client, thread_id: int) -> Tuple[bool, Optional[str]]:
    try:
        (trend_thread, _) = client.get_thread_page(id=thread_id, page=1)
    except anobbsclient.ResourceNotExistsException:
        return (False, "趋势串不存在")

    if trend_thread.marked_sage:
        return (False, "趋势串被SAGE")
    return (True, None)


if __name__ == "__main__":
    main(sys.argv)
