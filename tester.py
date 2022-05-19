# -*- encoding: utf-8 -*-
import time
import asyncio
import aiohttp
import aiohttp.client_exceptions
from loguru import logger
from multiprocessing import Process
# 导入redis
from database import RedisClient
# 导入自定义数据结构
from structure import Proxy
from structure import Headers
# 导入配置
from settings import CONCURRENT_QUANTITY
from settings import TEST_SLEEP_TIME


class TesterProcess(Process):
    '''测试进程'''
    def __init__(self, sleep_time: int=TEST_SLEEP_TIME, *args, **kwargs):
        super(TesterProcess, self).__init__(*args, **kwargs)
        # 休眠时长
        self.sleep_time = sleep_time
        # 任务列表
        self.tasks: list = None
        

    def run(self) -> None:
        # redis
        self.redis_cli = RedisClient()
        # 循环
        self.loop = asyncio.get_event_loop()
        # 队列集
        self._queue = asyncio.Queue()
        while True:
            logger.info("Tester start...")
            self.loop.run_until_complete(self.execute())
            logger.info("Tester Exit...")
            time.sleep(self.sleep_time)


    async def execute(self) -> None:
        '''执行'''
        workers = []
        for _ in range(CONCURRENT_QUANTITY):
            worker = self.loop.create_task(self.consumer())
            workers.append(worker)
        await self.loop.create_task(self.producer())
        await self._queue.join()


    async def producer(self) -> None:
        '''生产者'''
        cursor = 0
        while True:
            cursor, results = self.redis_cli.batch(cursor=cursor)
            for proxy in results:
                await self._queue.put(proxy)
            if not cursor:
                break


    async def consumer(self) -> None:
        '''消费者'''
        while True:
            proxy = await self._queue.get()
            try:
                await self.request(proxy)
            except Exception as exc:
                logger.error(f"{type(exc)}, {exc.args}")
            finally:
                self._queue.task_done()


    async def request(self, proxy: 'Proxy',**kwargs) -> None:
        '''异步请求'''
        # 请求头
        kwargs.setdefault("headers", Headers().random) 
        # 超时
        kwargs.setdefault("timeout", aiohttp.ClientTimeout(total=5))
        # 代理
        kwargs.setdefault("proxy", proxy.to_url())
        # 避免ssl证书问题
        conn = aiohttp.TCPConnector(ssl=False)
        # 发送请求
        logger.info(f"test => {proxy}")
        async with aiohttp.ClientSession(trust_env=True, connector=conn) as session:
            try:
                async with session.get("http://www.httpbin.org/ip", 
                                    **kwargs) as response:
                    response_json = await response.json()
                    # logger.warning(response.status)
            except Exception as exc:
                self.redis_cli.dec(proxy)
            else:
                origin = response_json.get("origin")
                if origin and origin.split(", ").__len__() > 1:
                    self.redis_cli.del_(proxy)
                    logger.debug("The {proxy} is not anonymous.")
                else:    
                    self.redis_cli.max(proxy)
                


if __name__ == "__main__":
    tester = TesterProcess(100)
    # tester.daemon = True
    tester.start()
    tester.join()