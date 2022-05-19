# -*- encoding: utf-8 -*-
# 配置文件

'''爬取进程配置'''
# 休眠时间，单位s
CRAWL_SLEEP_TIME = 100


'''数据库配置'''
# 域名
REDIS_HOST = "192.168.101.37"
# 端口
REDIS_PORT = 6379
# 密码
REDIS_PASSWORD = "718293"
# 存储对应字段名
REDIS_FIELD_NAEM = "proxies"
# 新IP默认分数
DEFAULT_SCORE = 10
# 最高分数
MAX_SCORE = 100
# 最低分数
MIN_SCORE = 0


'''测试进程'''
# 并发量
CONCURRENT_QUANTITY = 100
# 休眠时长
TEST_SLEEP_TIME = 20


'''web服务器配置'''
# 域名
APP_HOST = "localhost"
# 端口
APP_PORT = 8081
# 是否支持多线程
IS_THREADED = True