# -*- encoding: utf-8 -*-
import parsel
from structure import Proxy
from crawling.ProxySpiderBase import ProxySpiderBase
BASE_URL = "http://www.66ip.cn/{}.html"

class Free66Proxy(ProxySpiderBase):
    '''66免费代理'''
    urls = [BASE_URL.format(page) for page in range(2, 11)]
    urls.append(
        BASE_URL.format("index")
    )
    def parse(self, html: str) -> "Generator['Proxy or None']":
        root = parsel.Selector(html)
        for tr in root.xpath('''//table/tr'''):
            host = tr.xpath('''./td[1]/text()''').get()
            port = tr.xpath('''./td[2]/text()''').get()
            yield self.is_proxy(Proxy(host, port))

    
