# -*- encoding: utf-8 -*-
import parsel
from crawling.ProxySpiderBase import ProxySpiderBase
from structure import Proxy

BASE_URL = "http://www.kxdaili.com/dailiip/1/{}.html"

class KaiXinProxy(ProxySpiderBase):
    '''开心代理'''
    urls = [BASE_URL.format(page) for page in range(1, 11)]
    def parse(self, html: str) -> "Generator['Proxy or None']":
        root = parsel.Selector(html)
        for elements in root.xpath('''//table[@class="active"]/tbody/tr'''):
            host = elements.xpath('''./td[1]/text()''').get()
            port = elements.xpath('''./td[2]/text()''').get()
            yield self.is_proxy(Proxy(host, port))