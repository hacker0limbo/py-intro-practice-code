from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
)
from models.user import User

index_bp = Blueprint('index', __name__)


def current_user():
    """
    从 session 中找到 user_id 字段, 找不到返回 -1
    session 已经是加密的, 通过前面的 app.secret_key 加密
    返回 user, 没有为 None
    """
    uid = session.get('user_id', -1)
    u = User.query.get(uid)
    return u


@index_bp.route('/')
def index():
    """
    主页, 包括显示登录和注册
    """
    u = current_user()
    template = render_template('index.html', user=u)
    # 如果要写入 cookie, 必须使用 make_response 函数构造一个 response, 再对该响应添加 cookie
    res = make_response(template)
    res.set_cookie('cookie_name', 'limboer')
    return res


@index_bp.route('/register', methods=['POST'])
def register():
    form = request.form
    u  = User.register(form)
    return redirect(url_for('index.index'))


@index_bp.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('index.index'))
    else:
        # 写入 session
        session['user_id'] = u.id
        return redirect(url_for('index.profile'))


@index_bp.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    else:
        return render_template('profile.html', user=u)
