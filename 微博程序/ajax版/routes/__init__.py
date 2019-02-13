import json
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from routes.session import session

PATH = f'{Path(__file__).parent.parent}/views'
LOADER = FileSystemLoader(PATH)
env = Environment(loader=LOADER)


def template(name):
    """
    根据文件名返回 views 里面的 HTML 内容
    """
    path = 'views/' + name
    with open(path, 'r') as f:
        return f.read()


def j_template(path, **kwargs):
    """
    jinja 模板, 渲染并返回 HTML 字符串
    """
    t = env.get_template(path)
    return t.render(**kwargs)


def response_with_headers(headers: dict, code=200):
    """
    拼接返回响应的 headers, 参数如下是一个 dict, 如下:
    {
        Content-Type: text/html
        Set-Cookie: user=gua
    }
    返回响应的字符串形式
    """
    header = f'HTTP/1.1 {code} OK\r\n'
    header += ''.join([f'{k}: {v}\r\n' for k, v in headers.items()])
    return header


def redirect(url):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    headers = {
        'Location': url,
    }
    # 增加 Location 字段并生成 HTTP 响应返回
    # 注意, 没有 HTTP body 部分
    r = response_with_headers(headers, 302) + '\r\n'
    return r.encode('utf-8')


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
    注意, 可能会是其他静态文件, 比如 js, css, 可以根据 后缀名 设置不同的 Content-Type
    """
    filename = request.query.get('file', '')
    file_ext = filename.split('.')[-1]
    extensions = {
        'js': b'Content-Type: text/javascript\r\n',
        'css': b'Content-Type: text/css\r\n',
        'gif': b'Content-Type: image/gif\r\n',
    }
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\n'
        header += extensions.get(file_ext, b'')
        data = header + b'\r\n'+ f.read()
        return data


def http_response(body, headers=None):
    """
    返回 http 响应, 默认 body 为 HTML 格式
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    if headers is not None:
        header = response_with_headers(headers)
    response = header + '\r\n' + body
    return response.encode('utf-8')


def json_response(data):
    """
    返回 json 格式的 body 数据(页面)
    前端就可以发送 ajax 到该页面获取 json 格式的字符串

    data 为 列表或字典
    json.dumps 用于把 list 或者 dict 转化为 json 格式的字符串
    ensure_ascii=False 可以正确处理中文
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

