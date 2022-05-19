# -*- encoding: utf-8 -*-
import random 
import redis
from typing import Generator
from typing import Tuple
from loguru import logger
from structure import Proxy
# 导入配置
from settings import REDIS_HOST
from settings import REDIS_PORT
from settings import REDIS_PASSWORD
from settings import REDIS_FIELD_NAEM
from settings import DEFAULT_SCORE
from settings import MAX_SCORE
from settings import MIN_SCORE

class RedisClient(object):
    '''redis客户都'''
    def __init__(self, host: str=REDIS_HOST, port: int=REDIS_PORT, 
                 password: str=REDIS_PASSWORD, **kwargs):
        # decode_responses 表示存储类型str
        self.cli = redis.StrictRedis(
            host=host, 
            port=port, 
            password=password, 
            decode_responses=True, 
            **kwargs
        )


    def add(self, proxy: 'Proxy', field_name: str=REDIS_FIELD_NAEM, 
            score: int=DEFAULT_SCORE) -> int:
        '''
        添加代理到集合中
        return[int]: 1 => 添加成功, 0 => 添加失败。
        '''
        if self.exists(proxy) == True:
            logger.debug(f"repeat ip => {proxy}")
            return 0
        logger.info(f"add into => {proxy}")
        return self.cli.zadd(field_name, {str(proxy): score})
    

    def count(self, field_name: str=REDIS_FIELD_NAEM) -> int:
        '''获得总数'''
        return self.cli.zcard(field_name)


    def all(self, field_name: str=REDIS_FIELD_NAEM, 
            min: int=MIN_SCORE, max: int=MAX_SCORE) -> "Generator['Proxy']":
        '''获得集合中所有数据，并降序'''
        yield from Proxy.to_list(self.cli.zrangebyscore(field_name, min, max))


    def batch(self, field_name: str=REDIS_FIELD_NAEM, cursor: int=0
             ) -> '''Tuple[int, "List['Proxy']"]''':
        cursor, results = self.cli.zscan(field_name, cursor, count=20)
        return cursor, list(Proxy.to_list([item[0] for item in results]))


    def inc(self, proxy: 'Proxy', field_name: str=REDIS_FIELD_NAEM) -> float:
        '''自增'''
        return self.cli.zincrby(field_name, 1, str(proxy))


    def dec(self, proxy: 'Proxy', field_name: str=REDIS_FIELD_NAEM,
            min: int=MIN_SCORE) -> None:
        '''自减, 分数<=0删除值'''
        new_score = self.cli.zincrby(field_name, -1, str(proxy))
        logger.debug(f"Decrement {proxy} score 1.")
        if new_score <= min:
            self.del_(proxy)
            logger.debug(f"The {proxy} score is zero, deleted.")


    def del_(self, proxy: 'Proxy', field_name: str=REDIS_FIELD_NAEM) -> None:
        '''删除某值'''
        return self.cli.zrem(field_name, str(proxy))
        

    def exists(self, proxy: 'Proxy', field_name: str=REDIS_FIELD_NAEM) -> bool:
        '''
        判断某值是否存在
        return[int]: 存在 => True, 某则 => False.
        '''
        return self.cli.zscore(field_name, str(proxy)) is not None


    def max(self, proxy: 'Proxy', field_name: str=REDIS_FIELD_NAEM, 
            score: int=MAX_SCORE) -> int:
        '''设置代理ip分数为最大值'''
        logger.info(f"Set {proxy} score is one hundred score.")
        return self.cli.zadd(field_name, {str(proxy): score})

    
    def random(self, field_name: str=REDIS_FIELD_NAEM, max: int=MAX_SCORE) -> 'Proxy or None':
        '''
        随机从池里提取一IP
        策略: 先尝试提取100分的IP, 若空在全局随机提取。
        '''
        # 先去获取100分的
        results = list(self.all(min=max))
        if results:
            return random.choice(results)
            
        # 如果没有从全部分数中获取
        proxy = random.choice(self.batch()[1])
        if proxy:
            return proxy
        return None

    def __del__(self):
        self.cli.close()


if __name__ == "__main__":
    redis_cli = RedisClient()
    proxy = Proxy("8.8.8.8", "8888")
    # redis_cli.dec(proxy)
    print(redis_cli.exists(proxy))
    print(redis_cli.all())