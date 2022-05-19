# -*- coding: utf-8 -*-
# 请在当前路径"./crawling/proxy"创建你的爬虫扩展py文件
# 首先导入爬虫基类
from crawling.ProxySpiderBase import ProxySpiderBase
# 导入解析模块，这个随意，我习惯用parsel
import parsel
# 导入Proxy数据类型
from structure import Proxy
# 用来构建爬取url
BASE_URL = "https://www.dieniao.com/FreeProxy/{}.html"

class ButterflyBirdProxy(ProxySpiderBase):
    '''蝶鸟代理，请基础ProxySpiderBase爬虫基类'''
    # 提前创建好爬取链接
    urls = [BASE_URL.format(page) for page in range(1, 4)]
    def parse(self, html: str) -> "Generator['Proxy or None']":
        '''
        重构此方法，这个方法就是解析请求返回的响应内容
        不管如何解析，关键在于返回，方法是个生成器，注
        意返回内容类型为Proxy或None。
        '''
        root = parsel.Selector(html)
        li_xml_path = '''//li[@class="f-list col-lg-12 col-md-12 col-sm-12 col-xs-12"]'''
        for li_element in root.xpath(li_xml_path):
            # 域名字符串
            host_str = li_element.xpath('''./span[1]/text()''').get()
            # 端口字符串
            port_str = li_element.xpath('''./span[2]/text()''').get()
            # 关键在这里, 这个is_proxy是判断是不是非法的ip，如果是会强制返回None
            # 所以尽量调用self.is_proxy返回
            yield self.is_proxy(Proxy(host_str, port_str))