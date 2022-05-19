# -*- encoding: utf-8 -*-
import parsel
from structure import Proxy
from crawling.ProxySpiderBase import ProxySpiderBase

BASE_URL = "http://www.ip3366.net/?stype=1&page={}"

class CloudProxy(ProxySpiderBase):
    '''云代理'''
    urls = [BASE_URL.format(page) for page in range(1, 11)]
    def parse(self, html: str) -> "Generator['Proxy or None']":
        root = parsel.Selector(html)
        for tr in root.xpath('''//tbody/tr'''):
            host = tr.xpath('''./td[1]/text()''').get()
            port = tr.xpath('''./td[2]/text()''').get()
            yield self.is_proxy(Proxy(host, port))