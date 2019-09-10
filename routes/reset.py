import os
import uuid

# from celery.events import receiver
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

from config import admin_mail
from models.message import Messages, send_mail
from models.user import User
from routes import current_user, csrf_required, cache

import json

from utils import log

main = Blueprint('reset', __name__)


@csrf_required
@main.route('/view')
def index():
    return render_template('forgot-password.html')


@main.route('/send', methods=["POST"])
def send():
    # 获得用户名
    # 通过用户名获得用户id
    form = request.form.to_dict()
    name = form['username']
    # log('username', name)
    u = User.one(username=name)
    # u = current_user()
    # 生成token
    token = str(uuid.uuid4())

    # 普通存对应关系
    # csrf_tokens[token] = u.id
    id = u.id

    # 存对应关系
    cache.set(token, id)
    # 发送邮件
    # log('csrf_tokens', csrf_tokens)
    receiver: User = User.one(id=u.id)
    # reset_link = 'http://localhost:3000/reset/edit?token={}'.format(token)
    reset_link = 'http://49.235.39.6/reset/edit?token={}'.format(token)
    content = '点击链接重置密码：{}\n'.format(
        reset_link,
    )
    send_mail(
        subject='重置密码',
        author=admin_mail,
        to=receiver.email,
        content=content,
    )
    return render_template('login.html')


@main.route('/edit')
def update_view():
    return render_template('reset.html')


@csrf_required
@main.route('/update', methods=["POST", "GET"])
def update():
    form = request.form.to_dict()
    log('form', form)
    token = str(request.referrer).split('=')[-1]
    # log('token', token, request.referrer, csrf_tokens)
    # user_id = csrf_tokens[token]
    user_id = cache.get(token)
    u = User.one(id=user_id)
    new_password = User.salted_password(form['password'])
    User.update(u.id, password=new_password)

    return render_template('login.html')
