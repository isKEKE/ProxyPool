# -*- coding: utf-8 -*-
import asyncio
import time
import multiprocessing
from loguru import logger
# 导入redis
from database import RedisClient
# 导入配置
from settings import CRAWL_SLEEP_TIME
# 导入爬虫类列表
from crawling.proxy import __all__ as spider_cls_list


__doc__ = '''
免费代理: https://blog.csdn.net/u013762572/article/details/85646105
'''

class CrawlerProcess(multiprocessing.Process):
    '''爬虫进程'''
    def __init__(self, sleep_time: int=CRAWL_SLEEP_TIME):
        super(CrawlerProcess, self).__init__()
        self.sleep_time = sleep_time
        # 任务对象列表
        self.tasks: list = None



    @logger.catch
    def run(self) -> None:
        # redis 链接
        self.redis_cli = RedisClient()
        # 获得任务循环
        self.loop = asyncio.get_event_loop()

        while True:
            logger.info("Crawler Start")
            self.loop.run_until_complete(self.create_spider_tasks())
            logger.info("Crawler Exit.")    
            time.sleep(self.sleep_time)

    
    async def create_spider_tasks(self) -> None:
        '''创建线程'''
        self.tasks = []
        for ProxySpider in spider_cls_list:
            proxy_spider = ProxySpider(self.redis_cli)
            task = self.loop.create_task(proxy_spider.crawl())
            self.tasks.append(task)
        await asyncio.wait(self.tasks)


if __name__ == "__main__":
    crawler = CrawlerProcess()
    crawler.daemon = True
    crawler.start()
    crawler.join()
    pass