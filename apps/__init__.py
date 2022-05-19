# -*- encoding: utf-8 -*-
from flask import Flask
# 代理蓝图
from .proxy import proxy_bp

def create_app() -> 'Flask':
    '''app实例创建'''
    app = Flask(__name__)
    # 注册蓝图
    app.register_blueprint(proxy_bp)
    return app