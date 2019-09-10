import uuid
from functools import wraps

import redis
from flask import session, request, abort, redirect, url_for

from models.user import User
from models.topic import Topics
from utils import log


# def current_user():
#     if 'session_id' in request.cookies:
#         session_id = request.cookies['session_id']
#         s = Session.one_for_session_id(session_id=session_id)
#         key = 'session_id_{}'.format(session_id)
#         user_id = int(cache.get(key))
#         log('current_user key <{}> user_id <{}>'.format(key, user_id))
#         u = User.one(id=user_id)
#         return u
#     else:
#         return None

def current_user():
    # uid = session.get('user_id', '')
    # u: User = User.one(id=uid)
    # type annotation
    # User u = User.one(id=uid)
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        key = 'session_id_{}'.format(session_id)
        # 全部变为从 cache 获取信息
        user_id = int(cache.get(key))
        u = User.one(id=user_id)
        return u


# csrf_tokens = dict()


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # token = request.args['token']
        # u = current_user()
        # if token in csrf_tokens and csrf_tokens[token] == u.id:
        #     csrf_tokens.pop(token)
        #     return f(*args, **kwargs)
        # else:
        #     abort(401)

        token = request.args.get('token')
        u = current_user()
        log('token认证', token, u.id, cache.get(token))
        if cache.exists(token) and int(cache.get(token)) == u.id:
            cache.delete(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def author_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        u = current_user()
        topic_id = request.args.get('id')
        t = Topics.one(id=topic_id)
        log('删除作者认证，文章作者id {}， 操作人id {}'.format(topic_id, u.id))
        if t.user_id == u.id:
            log('作者', u)
            return f(*args, **kwargs)
        else:
            log('非作者本人')
            abort(401)

    return wrapper()


def new_csrf_token():
    # u = current_user()
    # token = str(uuid.uuid4())
    # csrf_tokens[token] = u.id
    # return token
    # redis
    u = current_user()
    token = str(uuid.uuid4())
    id = u.id
    # 存入位置变化了
    cache.set(token, id)
    return token


cache = redis.StrictRedis()
