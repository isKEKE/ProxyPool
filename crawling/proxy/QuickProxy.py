# -*- encoding: utf-8 -*-
import asyncio
import parsel
from structure import Proxy
from crawling.ProxySpiderBase import ProxySpiderBase

BASE_URL = "https://www.kuaidaili.com/free/inha/{}/"

class QuickProxy(ProxySpiderBase):
    '''快代理'''
    urls = [BASE_URL.format(page) for page in range(1, 11)]
    async def request(self, url, **kwargs) -> str:
        await asyncio.sleep(0.5)
        return await super().request(url, **kwargs)


    def parse(self, html: str) -> "Generator['Proxy or None']":
        '''解析'''
        selector = parsel.Selector(html)
        for tr in selector.xpath("//tr"):
            host = tr.xpath('./td[@data-title="IP"]/text()').get()
            port = tr.xpath('./td[@data-title="PORT"]/text()').get()
            yield self.is_proxy(Proxy(host, port))