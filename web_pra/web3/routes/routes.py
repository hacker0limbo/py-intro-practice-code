from models.message import Message
from models.user import User

def template(name):
    """
    根据文件名返回 views 里面的 HTML 内容
    """
    path = 'views/' + name
    with open(path, 'r') as f:
        return f.read()


def route_inex(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    response = header + '\r\n' + body
    return response.encode(encoding='utf-8')


def route_login(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        # 得到 post 过来的 body 数据
        form = request.form()
        # 根据发送来的数据创建一个对象, 和数据库里面的对象比较
        u = User(form)
        if u.validate_login():
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        # Get 请求, 打开这个页面的时候的处理
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    response = header + '\r\n' + body
    return response.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            u.save()
            result = f'注册成功<br> <pre>{u.all()}</pre>'
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
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

def route_index():
    pass

route_dict = {
    '/': route_index,
}
