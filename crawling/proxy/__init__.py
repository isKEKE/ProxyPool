# -*- encoding: utf-8 -*-
import pkgutil
import inspect 
from loguru import logger
from crawling.ProxySpiderBase import ProxySpiderBase

__all__ = __ALL__ = []

for finder, name, is_pkg in pkgutil.walk_packages(__path__):
    if is_pkg:
        continue
    try:
        module = finder.find_module(name).load_module(name)
    except Exception as exc:
        logger.warning(f"{type(exc)} => {exc.args}")
    else:
        for name, value in inspect.getmembers(module):
            # 添加到全局变量中
            globals()[name] = value
            if inspect.isclass(value) and issubclass(value, ProxySpiderBase) and \
                value is not ProxySpiderBase:
                __all__.append(value)
