# -*- encoding: utf-8 -*-
from attr import attrs
from typing import List


@attrs(auto_attribs=True)
class Proxy(object):
    '''代理IP结构体'''
    host: str
    port: str
    def __repr__(self) -> str:
        return str(self)
    

    def __str__(self) -> str:
        return f"{self.host}:{self.port}"


    def to_url(self) -> str:
        return f"http://{self.host}:{self.port}"
    

    @staticmethod
    def to_list(datas: 'List[str]') -> "Generator['Proxy']":
        '''redis返回ip字符串列表转换为Proxy对象列表'''
        for ip_str in datas:
            proxy = Proxy(*ip_str.split(":"))
            yield proxy
    

    

if __name__ == "__main__":
    proxy = Proxy("8.8.8.8", "8888")
    # print(proxy)
