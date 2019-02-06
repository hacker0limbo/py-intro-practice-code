from models.user import User
from routes.session import session
from utils import random_str
from routes import route_static, redirect, j_template, http_response


def current_user(request):
    """
    根据请求得到 cookie 并查看里面的 username, 没有的话说明还没有设置, 默认设置 session_id 为空
    username 默认为游客
    """
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')
    return username


def current_u(request):
    username = current_user(request)
    u = User.find_by(username=username)
    return u


def current_user_id(request):
    """
    根据发送的 cookie 得到 userid
    """
    username = current_user(request)
    u = User.find_by(username=username)
    if u is not None:
        return u.id
    return -1


def login_required(route_function):
    def func(request):
        uid = current_user_id(request)
        if uid == -1:
            # 没登录 不让看 重定向到 /login
            return redirect('/login')
        else:
            # 登录了, 正常返回路由函数响应
            return route_function(request)
    return func


def route_index(request):
    user_id = current_user_id(request)
    user = User.find_by(id=user_id)
    users = User.all()
    body = j_template('index.html', user=user, users=users)

    return http_response(body)


def route_login(request):
    """
    登录页面的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': 'a=b; c=d'
    }
    # username 默认是有课, session_id 默认是 ''
    username = current_user(request)

    if request.method == 'POST':
        # 得到 post 过来的 body 数据
        # 说明是第一次登录
        form = request.form()
        # 根据发送来的数据创建一个对象, 和数据库里面的对象比较
        u = User(form)
        if u.validate_login():
            session_id = random_str()
            session[session_id] = u.username
            # session 变为 {'fdsafeaf1213': '游客注册的用户名'}
            headers['Set-Cookie'] = f'user={session_id}'
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        # Get 请求, 打开这个页面的时候的处理
        result = ''
    body = j_template('login.html', username=username, result=result)
    # 拼接 header
    return http_response(body, headers=headers)


def route_register(request):
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register() is not None:
            result = f'注册成功<br> <pre>{User.all()}</pre>'
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = j_template('register.html', result=result)
    return http_response(body)


@login_required
def route_profile(request):
    """
    显示用户的个人信息界面

    判断, 如果没有登录, 重定向到登录页面登录
    若登录了就返回个人信息
    """
    username = current_user(request)
    u = User.find_by(username=username)
    body = j_template('profile.html', user=u)
    return http_response(body)


route_dict = {
    '/': route_index,
    '/static': route_static,
    '/login': route_login,
    '/register': route_register,
    '/profile': route_profile,
}
