#!/usr/bin/env python3
from typing import List
from dataclasses import dataclass
import itertools

import logging
import argparse
import sys

from datetime import datetime

from commonargs import parse_args, Arguments
from setuplogger import setup_aqt_logger

import anobbsclient


@dataclass
class CollectArguments(Arguments):
    time_since: datetime

    @staticmethod
    def _parse_extra_args(parser: argparse.ArgumentParser):
        parser.add_argument("-r", "--time-since", metavar="<2006-01-02 15:04:05-07:00>",
                            help="统计到的时间，RFC3339 格式，需带时区。",
                            type=datetime.fromisoformat, dest="range")


def main(args: List[str]):
    args: CollectArguments = parse_args(
        prog=args[0],
        args=args[1:],
        description="采集跑团版串",
        args_cls=CollectArguments,
    )
    assert(args.time_since.tzinfo != None)

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

    execute(args, client)


def execute(args: CollectArguments, client: anobbsclient.Client):

    logger = setup_aqt_logger(
        name="collect",
        base_log_folder_path=args.base_log_folder_path,
        tz=args.time_zone,
    )

    total_bandwidth_usage = anobbsclient.BandwidthUsage(0, 0)
    logger.info(f"将获取包含「自给定时间起有新活动的串」的页面。指定时间：{args.time_since}")
    for (round, n, page, bandwidth_usage) in walk_board_page(logger, client, args.board_id, args.time_since):
        logger.info(f"已获取版块页面：第 {round} 轮第 {n} 页。本页流量：{bandwidth_usage}")
        total_bandwidth_usage = anobbsclient.BandwidthUsage(
            *map(sum, zip(total_bandwidth_usage, bandwidth_usage)))
        # TODO
    logger.info(f"已完成获取版块页面。获取页面总计流量：{total_bandwidth_usage}")


def walk_board_page(logger: logging.Logger, client: anobbsclient.Client, board_id: int, since: datetime):
    for round in itertools.count(1):
        page_1_latest_modified_time = None
        for n in itertools.count(1):
            (page, bandwidth_usage) = client.get_board_page(board_id, n)
            yield (round, n, page, bandwidth_usage)
            if n == 1:
                page_1_latest_modified_time = max(
                    map(lambda thread: thread.last_modified_time, page))
            if page[-1].last_modified_time < since:
                if n == 1:
                    return
                else:
                    since = page_1_latest_modified_time
                    break


if __name__ == "__main__":
    main(sys.argv)
