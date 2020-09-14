#!/usr/bin/env python3
from typing import List
from dataclasses import dataclass

import logging
import argparse
import sys

from commonargs import parse_args, Arguments
from setuplogger import setup_aqt_logger

import anobbsclient


@dataclass
class CollectArguments(Arguments):
    pass


def main(args: List[str]):
    args = parse_args(
        prog=args[0],
        args=args[1:],
        description="采集跑团版串",
        args_cls=CollectArguments,
    )

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
    )

    logger.info("test")
    logger.debug("test")


if __name__ == "__main__":
    main(sys.argv)
