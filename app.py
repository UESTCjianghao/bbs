#!/usr/bin/env python3
import time
from encodings import undefined

from flask import Flask
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView

import secret
import config
from models.base_model import db
from models.user import User
from models.topic import Topics
from models.reply import Replys
from models.message import Messages
from models.board import Board

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
from routes.message import main as mail_routes
from routes.setting import main as setting_routes
from routes.reset import main as reset_routes
from utils import log


def count(input):
    log('count using jinja filter')
    return len(input)


def format_time(unix_timestamp):
    # enum Year():
    #     2013
    #     13
    # f = Year.2013
    f = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(unix_timestamp)
    formatted = time.strftime(f, value)
    return formatted


# class UserModelView(ModelView):
#     column_searchable_list = ('username', 'password')


def configured_app():
    # web framework
    # web application
    # __main__
    app = Flask(__name__)
    # 设置 secret_key 来使用 flask 自带的 session
    # 这个字符串随便你设置什么内容都可以
    app.secret_key = secret.secret_key

    uri = 'mysql+pymysql://root:{}@localhost/web21?charset=utf8mb4'.format(
        secret.database_password
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.template_filter()(count)
    app.template_filter()(format_time)

    # 后台管理
    # admin = Admin(app, name='web20 admin', template_mode='bootstrap3')
    # mv = UserModelView(User, db.session)
    # admin.add_view(mv)
    # mv = ModelView(Board, db.session)
    # admin.add_view(mv)
    # mv = ModelView(Topics, db.session)
    # admin.add_view(mv)
    # mv = ModelView(Replys, db.session)
    # admin.add_view(mv)
    # mv = ModelView(Messages, db.session)
    # admin.add_view(mv)

    register_routes(app)
    return app


def register_routes(app):
    """
    在 flask 中，模块化路由的功能由 蓝图（Blueprints）提供
    蓝图可以拥有自己的静态资源路径、模板路径（现在还没涉及）
    用法如下
    """
    # 注册蓝图
    # 有一个 url_prefix 可以用来给蓝图中的每个路由加一个前缀

    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    # app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(mail_routes, url_prefix='/message')
    app.register_blueprint(setting_routes, url_prefix='/setting')
    app.register_blueprint(reset_routes, url_prefix='/reset')


# 运行代码
if __name__ == '__main__':
    app = configured_app()
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    # 自动 reload jinja
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=3000,
        threaded=True,
    )
    app.run(**config)
