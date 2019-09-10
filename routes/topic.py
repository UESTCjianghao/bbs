from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.topic import Topics
from models.board import Board

main = Blueprint('topic', __name__)


@main.route("/")
def index():
    u = current_user()
    if u is not None:
        board_id = int(request.args.get('board_id', -1))
        if board_id == -1:
            ms = Topics.all()
        else:
            ms = Topics.all(board_id=board_id)
        token = new_csrf_token()
        bs = Board.all()
        u = current_user()
        return render_template('topic/index.html', ms=ms, token=token, bs=bs, bid=board_id, user=u)
    else:
        return render_template('login.html')


@main.route('/<int:id>')
def detail(id):
    m = Topics.get(id)
    b = Board.one(id=m.board_id)
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m, b=b)


@main.route("/delete")
@csrf_required
# @author_required
def delete():
    id = int(request.args.get('id'))
    u = current_user()
    print('删除 topic 用户是', u, id)
    Topics.delete(id)
    return redirect(url_for('.index'))


@main.route("/new")
def new():
    # print('board id', request.args.get('board_id'))
    board_id = int(request.args.get('board_id'))
    bs = Board.all()
    # return render_template("topic/new.html", bs=bs, bid=board_id)
    token = new_csrf_token()
    # token =
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id)


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    Topics.new(form, user_id=u.id)
    return redirect(url_for('.index'))
