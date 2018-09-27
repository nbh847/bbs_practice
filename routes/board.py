from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.board import Board

main = Blueprint('board', __name__)


@main.route('/admin')
def index():
    return render_template('board/admin_index.html')
    ...


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    if u.role == 1:
        print('is admin')
        m = Board.new(form)
        print('DEBUG', form)
    else:
        print('not admin')
    return redirect(url_for('topic.index'))


@main.route("/delete", methods=["POST"])
def delete():
    form = request.form
    board_id = int(form.get('title', -1))
    u = current_user()
    if u.role == 1:
        print('is admin')
        m = Board.delete(board_id)
        print('DEBUG, delete success', form)
    else:
        print('not admin, delete failed')
    return redirect(url_for('topic.index'))
