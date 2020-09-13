#!/usr/bin/env python3
from typing import List
from dataclasses import dataclass

import logging
import argparse
import sys

from commonargs import parse_args, Arguments
from setuplogger import setup_logger


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

    execute(args)


def execute(args: CollectArguments):

    logger = setup_logger(
        name="AQT.collect",  # AQT = adnmb_quests_trend
        base_log_folder_path=args.base_log_folder_path,
    )

    logger.info("test")
    logger.debug("test")


if __name__ == "__main__":
    main(sys.argv)
