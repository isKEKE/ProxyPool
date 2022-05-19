# -*- encoding: utf-8 -*-
import sys
import os
from loguru import logger
from tester import TesterProcess
from crawler import CrawlerProcess
from server import WebServer


# 日志配置
logger.remove()
os.path.exists("./log") or os.makedirs("./log")
logger.add(sys.stdout, level="INFO")
logger.add("./log/running.log", level="DEBUG")
logger.add("./log/error.log", level="ERROR")


def main() -> int:
    '''运行'''
    __process__ = []

    for process_cls in [CrawlerProcess, TesterProcess, WebServer]:
        process = process_cls()
        process.daemon = True
        process.start()
        __process__.append(process)


    for process in __process__:
        process.join()

    return 0


if __name__ == "__main__":
    main()