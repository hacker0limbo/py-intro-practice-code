from models import open_db, close_db
from models.user import User
from models.weibo import Weibo, Comment

from routes import j_template, redirect, error, http_response
from routes.routes import current_user_id, login_required


def index(request):
    """
    用户 weibo 的主页, 前往路径为 /weibo/index?user_id=1
    该页面不登录也可以访问
    """
    user_id = int(request.query.get('user_id', -1))
    user = User.find_by(id=user_id)
    if user is None:
        return redirect('/login')
    weibos = Weibo.find_all(user_id=user_id)
    # 找到 user 发布的所有 weibo
    body = j_template('weibo_index.html', user=user, weibos=weibos)
    return http_response(body)


def new(request):
    """
    添加新微博的页面, 路径为 /weibo/new
    """
    user_id = int(current_user_id(request))
    user = User.find_by(id=user_id)
    if user is None:
        return redirect('/login')
    # 找到 user 发布的所有 weibo
    body = j_template('weibo_new.html', user=user)
    return http_response(body)


def add(request):
    """
    新微博发送的数据在这里处理
    """
    conn, cursor = open_db()
    form = request.form()
    uid = form.get('user_id', -1)
    weibo = Weibo(form)
    weibo.user_id = int(uid)
    Weibo.add(cursor, weibo)
    close_db(conn, cursor)
    return redirect(f'/weibo/index?user_id={str(uid)}')


def delete(request):
    """
    删除一个 weibo
    """
    uid = current_user_id(request)
    weibo_id = int(request.query.get('id', -1))
    conn, cursor = open_db()
    Weibo.delete(cursor, weibo_id)
    close_db(conn, cursor)
    return redirect(f'/weibo/index?user_id={str(uid)}')


def edit(request):
    """
    更新 weibo 的主页, 前往路径为 /weibo/edit?user_id=1
    """
    weibo_id = int(request.query.get('id', -1))
    weibo = Weibo.find_by(id=weibo_id)
    if weibo is None:
        return redirect('/login')
    # 找到 user 发布的所有 weibo
    body = j_template('weibo_edit.html', weibo=weibo)
    return http_response(body)


def update(request):
    """
    更新微博的数据在这里处理
    """
    uid = current_user_id(request)
    form = request.form()
    weibo_id = int(form.get('id', -1))
    weibo_content = form.get('content', '')
    conn, cursor = open_db()
    Weibo.update(cursor, weibo_id, weibo_content)
    close_db(conn, cursor)
    return redirect(f'/weibo/index?user_id={str(uid)}')


def comment_add(request):
    """
    增加 一个评论
    """
    uid = current_user_id(request)
    form = request.form()
    weibo_id = form.get('weibo_id', -1)
    new_form = {
        'weibo_id': weibo_id,
        'user_id': uid,
    }
    form.update(new_form)
    comment = Comment(form)

    conn, cursor = open_db()
    Comment.add(cursor, comment)
    close_db(conn, cursor)
    return redirect(f'/weibo/index?user_id={str(uid)}')


route_dict = {
    '/weibo/index': index,
    '/weibo/new': login_required(new),
    '/weibo/edit': login_required(edit),
    '/weibo/add': login_required(add),
    '/weibo/update': login_required(update),
    '/weibo/delete': login_required(delete),
    '/comment/add': login_required(comment_add),
}