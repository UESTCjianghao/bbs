import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory,
    current_app)
from werkzeug.datastructures import FileStorage

from models.user import User
from routes import current_user, csrf_required

import json

from utils import log

main = Blueprint('setting', __name__)

"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""

import gevent
import time


@main.route("/")
def index():
    # t = threading.Thread()
    # t.start()
    # gevent.spawn()
    time.sleep(0.5)
    print('time type', time.sleep, gevent.sleep)
    u = current_user()
    return render_template("setting.html", user=u)


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file: FileStorage = request.files['avatar']
    # file = request.files['avatar']
    # filename = file.filename
    # ../../root/.ssh/authorized_keys
    # images/../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    if suffix not in ['gif', 'jpg', 'jpeg']:
        abort(400)
        log('不接受的后缀, {}'.format(suffix))
    else:
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        path = os.path.join('images', filename)
        file.save(path)

        u = current_user()
        User.update(u.id, image='/images/{}'.format(filename))

        return redirect(url_for('index.profile'))


@main.route('/images/<filename>')
def image(filename):
    # 不要直接拼接路由，不安全，比如
    # http://localhost:3000/images/..%5Capp.py
    # path = os.path.join('images', filename)
    # print('images path', path)
    # return open(path, 'rb').read()
    # if filename in os.listdir('images'):
    #     return
    return send_from_directory('images', filename)


@main.route('/re_info', methods=['POST'])
def re_info():
    form = request.form
    u = current_user()
    if form['username'] != '':
        User.update(u.id, username=form['username'])

    if form['sign'] != '':
        User.update(u.id, sign=form['sign'])

    return render_template("setting.html", user=u)


@csrf_required
@main.route('/password', methods=["POST"])
def update():
    form = request.form
    log('form', form)
    u = current_user()
    new_password = User.salted_password(form['password'])
    User.update(u.id, password=new_password)

    return render_template("login.html")
