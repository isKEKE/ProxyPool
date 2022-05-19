# -*- encoding: utf-8 -*-
import fake_useragent
from attr import attrs

@attrs(auto_attribs=True, slots=True)
class Headers(object):
    '''请求头'''
    _fake_ua: 'fake_useragent.UserAgent' = fake_useragent.UserAgent()
    _headers: dict = {}
    __instance__ = None
    def __new__(cls: 'Headers', *args, **kwargs) -> 'Headers':
        '''单例模式，减少开销'''
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls, *args, **kwargs)
        return cls.__instance__


    @property
    def random(self) -> dict:
        '''随机UA模式'''
        self._headers["User-Agent"] = self._fake_ua.random
        return self._headers



if __name__ == "__main__":
    header1 = Headers()
    header2 = Headers()
    print(header1, id(header1))
    print(header1.random, end="\n\n")
    print(header2, id(header2))
    print(header2.random, end="\n\n")
    print(header1.__slots__)
    