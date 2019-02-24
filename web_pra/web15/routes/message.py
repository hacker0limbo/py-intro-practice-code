from models.message import Message
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

message_bp = Blueprint('message', __name__)


@message_bp.route('/')
def index():
    messages = Message.query.all()
    return render_template('message.html', messages=messages)


@message_bp.route('/add', methods=['POST'])
def add():
    form = request.form
    m = Message(form)
    Message.add(m)
    return redirect(url_for('message.index'))


@message_bp.route('/delete/<int:message_id>', methods=['GET'])
def delete(message_id):
    m = Message.delete(message_id)
    return redirect(url_for('message.index'))