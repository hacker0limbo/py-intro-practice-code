from models.message import Message
from models.user import User
from session import session
from utils import random_str
from routes import template, response_with_headers, route_static, redirect, j_template


def current_user(request):
    """
    根据请求得到 cookie 并查看里面的 username, 没有的话说明还没有设置, 默认设置 session_id 为空
    username 默认为游客
    """
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')
    return username


def current_user_id(request):
    """
    根据发送的 cookie 得到 userid
    :param request:
    :return:
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
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    user_id = current_user_id(request)
    user = User.find_by(id=user_id)
    body = j_template('index.html', user=user)

    response = header + '\r\n' + body
    return response.encode(encoding='utf-8')


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
    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    # 拼接 header
    header = response_with_headers(headers)
    response = header + '\r\n' + body
    return response.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register() is not None:
            result = f'注册成功<br> <pre>{User.all()}</pre>'
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_profile(request):
    """
    显示用户的个人信息界面

    判断, 如果没有登录, 重定向到登录页面登录
    若登录了就返回个人信息
    """
    username = current_user(request)
    print('username', username)
    if username != '游客':
        # 登录成功
        u = User.find_by(username=username)
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        body = template('profile.html')
        body = body.replace('{{id}}', str(u.id))
        body = body.replace('{{username}}', u.username)
        body = body.replace('{{note}}', u.note)
        r = header + '\r\n' + body
        return r.encode(encoding='utf-8')
    else:
        # 未登录
        header = 'HTTP/1/1 302 Moved\r\nContent-Type: text/html\r\nLocation: /login\r\n'
        r = header + '\r\n'
        return r.encode(encoding='utf-8')


def route_message(request):
    if request.method == 'POST':
        form = request.form()
        msg = Message(form)
        Message.add(msg)
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('msg.html')
    msgs = '<br>'.join([str(m) for m in Message.all()])
    body = body.replace('{{messages}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


route_dict = {
    '/': route_index,
    '/static': route_static,
    '/login': route_login,
    '/register': route_register,
    '/profile': route_profile,
    '/messages': route_message,
}
