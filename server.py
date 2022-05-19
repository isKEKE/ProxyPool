# -*- encoding: utf-8 -*-
from multiprocessing import Process
from loguru import logger
# 创建app函数
from apps import create_app
# 导入配置
from settings import APP_HOST
from settings import APP_PORT
from settings import IS_THREADED


class WebServer(Process):
    '''web服务, 用来获取代理IP'''
    def __init__(self):
        super(WebServer, self).__init__()
        # app对象
        self.app: 'Flask' = None
    
    @logger.catch
    def run(self) -> None:
        self.app = create_app()
        # 让flask支持协程
        self.app.run(host=APP_HOST, port=APP_PORT, threaded=IS_THREADED)


if __name__ == "__main__":
    web = WebServer()
    web.start()
    web.join()