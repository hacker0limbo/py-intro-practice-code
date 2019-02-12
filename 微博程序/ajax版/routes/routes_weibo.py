from models.user import User
from models.weibo import Weibo, Comment

from routes import j_template, redirect, error, http_response
from routes.routes import current_user_id, login_required, current_u


def index(request):
    """
    用户 weibo 的主页, 前往路径为 /weibo/index?user_id=1
    该页面不登录也可以访问
    """
    current = False
    user_id = int(request.query.get('user_id', -1))
    u_id = int(current_user_id(request))
    if u_id is not None and u_id == user_id:
        # 说明当前用户不是该微博的主人
        current = True
    user = User.find_by(id=user_id)
    weibos = Weibo.find_all(user_id=user_id)
    # 找到 user 发布的所有 weibo
    body = j_template('weibo_index.html', user=user, weibos=weibos, current=current)
    return http_response(body)


@login_required
def new(request):
    """
    添加新微博的页面, 路径为 /weibo/new
    """
    user = current_u(request)
    # 找到 user 发布的所有 weibo
    body = j_template('weibo_new.html', user=user)
    return http_response(body)


@login_required
def add(request):
    """
    新微博发送的数据在这里处理
    """
    form = request.form()
    uid = form.get('user_id', -1)
    weibo = Weibo(form)
    weibo.user_id = int(uid)
    Weibo.add(weibo)
    return redirect(f'/weibo/index?user_id={str(uid)}')


@login_required
def delete(request):
    """
    删除一个 weibo
    """
    uid = current_user_id(request)
    weibo_id = int(request.query.get('id', -1))
    Weibo.delete(weibo_id)
    return redirect(f'/weibo/index?user_id={str(uid)}')


@login_required
def edit(request):
    """
    更新 weibo 的主页, 前往路径为 /weibo/edit?user_id=1
    """
    weibo_id = int(request.query.get('id', -1))
    weibo = Weibo.find_by(id=weibo_id)
    # 找到 user 发布的所有 weibo
    body = j_template('weibo_edit.html', weibo=weibo)
    return http_response(body)


@login_required
def update(request):
    """
    更新微博的数据在这里处理
    """
    uid = current_user_id(request)
    form = request.form()
    weibo_id = int(form.get('id', -1))
    weibo_content = form.get('content', '')
    Weibo.update(weibo_id, content=weibo_content)
    return redirect(f'/weibo/index?user_id={str(uid)}')


@login_required
def comment_add(request):
    """
    增加 一个评论
    """
    uid = current_user_id(request)
    weibo_u_id = int(request.query.get('user_id', -1))
    form = request.form()
    weibo_id = form.get('weibo_id', -1)
    new_form = {
        'weibo_id': weibo_id,
        'user_id': uid,
    }
    form.update(new_form)
    comment = Comment(form)

    Comment.add(comment)
    return redirect(f'/weibo/index?user_id={str(weibo_u_id)}')


route_dict = {
    '/weibo/index': index,
    '/weibo/new': new,
    '/weibo/edit': edit,
    '/weibo/add': add,
    '/weibo/update': update,
    '/weibo/delete': delete,
    '/comment/add': comment_add,
}
