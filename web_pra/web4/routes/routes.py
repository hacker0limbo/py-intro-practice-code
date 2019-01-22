from models.message import Message
from models.user import User
from session import session
from utils import random_str

def template(name):
    """
    根据文件名返回 views 里面的 HTML 内容
    """
    path = 'views/' + name
    with open(path, 'r') as f:
        return f.read()


def current_user(request):
    """
    根据请求得到 cookie 并查看里面的 username, 没有的话说明还没有设置, 默认设置 session_id 为空
    username 默认为游客
    """
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')
    return username


def route_static(request):
    """
    静态资源处理
    过程如下:
    <img src="/static?file=doge.gif">
    发送 GET 请求到 /static?file=doge.gif
    GET /static?file=doge.gif
    path 解析完成, 分离 path 和 query
        query = {
            'file', 'doge.gif',
        }
    被路由捕获, 调用该函数
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n'+ f.read()
        return img


def response_with_headers(headers: dict):
    """
    拼接返回响应的 headers, 参数如下是一个 dict, 如下:
    {
        Content-Type: text/html
        Set-Cookie: user=gua
    }
    返回响应的字符串形式
    """
    header = 'HTTP/1.1 200 OK\r\n'
    header += ''.join([f'{k}: {v}\r\n' for k, v in headers.items()])
    return header


def route_index(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    username = current_user(request)
    body = body.replace('{{username}}', username)
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
        if u.validate_register():
            User.add(u)
            # add 已经自动保存了
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


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 之前上课我说过不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


route_dict = {
    '/': route_index,
    '/static': route_static,
    '/login': route_login,
    '/register': route_register,
    '/profile': route_profile,
    '/messages': route_message,
}
