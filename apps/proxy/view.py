# -*- encoding: utf-8 -*-
from flask import Blueprint
from flask import jsonify
# 模块
from .modules import get_redis

# 蓝图
proxy_bp = Blueprint("proxy", __name__)


@proxy_bp.route("/")
def index() -> 'jsonify':
    '''主页'''
    return jsonify(code=200, msg="Easy Proxy Pool.")

@proxy_bp.route("/random")
def random_() -> 'jsonify':
    '''返回随机IP'''
    proxy = get_redis().random()
    return jsonify(code=200, msg="success", data=str(proxy))


@proxy_bp.route("/count")
def count() -> 'jsonify':
    '''返回数据库IP数量'''
    count = get_redis().count()
    return jsonify(code=200, msg="success", data=count)


@proxy_bp.route("/all")
def all() -> 'jsonify':
    '''返回数据库中所有的IP'''
    all_ = [str(proxy) for proxy in get_redis().all()]
    return jsonify(code=200, msg="success", data=all_)