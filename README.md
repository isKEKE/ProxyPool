# IP代理池

## 前言

## 一、环境搭建

#### 1.1 开发系统

> Ubuntu18.04; 但在Window 10 x64测试已经运行成功。

#### 1.2 Python

> 版本：`3.8.10`; 这里只是建议，我开发环境是`3.6.9`

- ```shell
  # 到项目根目录，执行此命令安装包
  $ pip install -r requirements.txt
  ```

#### 1.3 Redis

> 引用：https://www.cnblogs.com/ysocean/p/9074353.html

## 二、项目介绍

#### 2.1 思维导图

![ProxyPool](http://raw.staticdn.net/iskeke/images/main/blog/202205182248415.jpeg)

#### 2.2 文本描述

此项目分为一个主进程和三个子进程。主进程就是启动调度用，关键在于子进程，分别：`Crawler`爬虫进程、`Tester`测试进程、`Server`Web服务进程。

- 爬虫进程：定时的进行并发的爬取N个免费IP代理站点上的IP，并存储到Redis数据库；
- 测试进程：定时的进行并发测试Redis数据库中的IP；
- Web服务进程：为用户提取IP方便提供接口。

#### 2.3 目录描述

| 路径          | 描述                           |
| ------------- | ------------------------------ |
| ./apps        | 主要Web服务相关模块            |
| ./crawling    | 增量式爬取IP相关的爬虫模块     |
| ./database    | Redis数据库客户端模块          |
| ./log         | 日志保存位置                   |
| ./structure   | 自定义数据结构相关模块         |
| ./crawler.py  | **爬虫进程主模块**             |
| ./tester.py   | **测试进程主模块**             |
| ./server.py   | **Web进程主模块**              |
| ./settings.py | 脚本配置参数文件               |
| **./main.py** | **主进程，调度启动所有子进程** |

## 三、爬虫扩展

> 爬取IP站点扩展编写模板

- 这里以`蝶鸟IP`为列子

- ```python
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
  ```

## 四、知识要点

> 通过刨析大佬代码学到的知识点

- [关于attrs库的研究笔记]()

- [协程爬虫的一些知识要点(PS: 这里我还没写完这个东西知识点很多!)]()

## 五、作者声明&&建议

> 作者：珂珂

​		本人声明如果代码有任何的侵权，请及时联系我！我的思路来自于崔庆才老师《Python 3网络爬虫开发实战（第2版）》的第九章老师提供的代码进行学习而编写的此项目，所有思路可以说是相同，只是很多地方编写的方式不同！所以建议去看且使用大佬编写项目！

​		本人只是对于编程热爱进行自学，所以此项目有任何BUG麻烦及时告知我，我尽量进行解决！PS：本人也挺菜的。

​		我的建议是观看崔老师的书进行自己编写此项目，这样对自己的编写代码提供非常大的经验，当成功自己实现预想的目标成就感爆棚！

- 大佬项目github地址：https://github.com/Python3WebSpider/ProxyPool

- 我的Email: `li_99999@126.com` 
