# -*- encoding: utf-8 -*-
import re
import asyncio
import aiohttp
import aiohttp.client_exceptions
from typing import Generator
from loguru import logger
from structure import Headers

# 异常
request_exceptions = (
    asyncio.TimeoutError,
    aiohttp.client_exceptions.TooManyRedirects
)

class ProxySpiderBase(object):
    '''代理爬虫基类'''
    urls: list = None
    def __init__(self, cli: 'RedisClient'):
        self.cli = cli

    async def request(self, url, **kwargs) -> str:
        '''请求, 返回源码'''
        # 请求头
        kwargs.setdefault("headers", Headers().random) 
        # 超时
        kwargs.setdefault("timeout", aiohttp.ClientTimeout(total=5))
        # 避免ssl证书问题
        conn = aiohttp.TCPConnector(ssl=False)
        # 发送请求
        try:
            async with aiohttp.ClientSession(connector=conn) as session:
                async with session.get(url, **kwargs) as response:
                    html = await response.text()
                    return html
        except request_exceptions:
            return 


    def parse(self, html: str) -> "Generator['Proxy or None']":
        '''解析, 是个生成器'''
        raise AttributeError("基类不可直接调用，请重构")


    @logger.catch
    async def crawl(self) -> None:
        '''抓取'''
        for url in self.urls:
            logger.info(f"crawling url => {url}")
            html = await self.request(url)
            if html is None:
                continue
            for proxy in self.parse(html):
                if proxy is None:
                    continue
                self.cli.add(proxy)


    @staticmethod
    def is_proxy(proxy: 'Proxy') -> 'Proxy or None':
        '''判断是否是合法的代理'''
        is_result = re.match("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", str(proxy))
        if is_result is None:
            return None
        else:
            return proxy


if __name__ == "__main__":
    pass