# -*- encoding: utf-8 -*-
import parsel
from crawling.ProxySpiderBase import ProxySpiderBase
from structure import Proxy

BASE_URL = "https://www.tyhttp.com/free/page{}/"

class SunProxy(ProxySpiderBase):
    '''太阳HTTP代理'''
    urls = [BASE_URL.format(page) for page in range(1, 11)]
    def parse(self, html: str) -> "Generator['Proxy or None']":
        '''解析'''
        root = parsel.Selector(html)
        for elements in root.xpath('''//div[@class="tr ip_tr"]'''):
            host = elements.xpath('''./div[@class="td td-4"]/text()''').get()
            port = elements.xpath('''./div[@class="td td-2"]/text()''').get()
            yield self.is_proxy(Proxy(host, port))
