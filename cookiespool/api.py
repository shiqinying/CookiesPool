import json
from flask import Flask, g
from cookiespool.config import *
from cookiespool.db import *

__all__ = ['app']

app = Flask(__name__)

@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'


def get_conn():
    """
    获取
    :return:
    """
    for website in GENERATOR_MAP:
        print(website)
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website + '")'))
            setattr(g, website + '_accounts', eval('RedisClient' + '("accounts", "' + website + '")'))
    return g


@app.route('/<website>/random')
def random(website):
    """
    获取随机的Cookie, 访问地址如 /weibo/random
    :return: 随机Cookie
    """
    g = get_conn() #每次请求都会创建一个RedisClient连接对象，需要优化，启动程序时创建RedisClient对象，并绑定到g对象（可以考虑在__init__中实现），或者考虑RedisClient对象不再被引用时会不会自动断开连接？？？
    cookies = getattr(g, website + '_cookies').random()
    return cookies


@app.route('/<website>/add/<username>/<password>')
def add(website, username, password):
    """
    添加用户, 访问地址如 /weibo/add/user/password
    :param website: 站点
    :param username: 用户名
    :param password: 密码
    :return: 
    """
    g = get_conn()
    print(username, password)
    getattr(g, website + '_accounts').set(username, password)
    return json.dumps({'status': '1'})


@app.route('/<website>/count')
def count(website):
    """
    获取Cookies总数
    """
    g = get_conn()
    count = getattr(g, website + '_cookies').count()
    return json.dumps({'status': '1', 'count': count})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
