from flask import (
    render_template,
    request,
    redirect,
    url_for,
    abort,
    Blueprint,
)

from routes import *

import uuid
from models.topic import Topic
from models.board import Board

from models.topic import Topic

main = Blueprint('topic', __name__)

csrf_tokens = set()


@main.route("/")
def index():
    user = current_user()
    board_id = int(request.args.get('board_id', 0))
    if board_id:
        print('is board id :{}'.format(board_id))
        ms = Topic().find_all(board_id=board_id)
    else:
        print('not board id: {}'.format(board_id))
        ms = Topic().all()
    bs = Board.all()
    token = str(uuid.uuid4())
    csrf_tokens.add(token)
    return render_template("topic/index.html", ms=ms, bs=bs, user=user, token=token)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    board_id = m.board_id
    print('board id: {}'.format(board_id))
    print('type board id: {}'.format(type(board_id)))
    board = Board.get(board_id)
    print('({})'.format(board))
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m, board=board)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
def delete():
    token = request.args.get('token')
    if token in csrf_tokens:
        csrf_tokens.remove(token)
        id = int(request.args.get('id'))
        u = current_user()
        if u is not None:
            Topic.delete(id)
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        abort(403)


@main.route("/new")
def new():
    bs = Board.all()
    return render_template("topic/new.html", bs=bs)
