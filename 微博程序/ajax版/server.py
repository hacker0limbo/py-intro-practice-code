import socket
import json
from urllib.parse import urlparse, unquote, parse_qs
from routes import error
from routes.routes import route_dict
from routes.routes_todo import route_dict as todo_route
from routes.routes_weibo import route_dict as weibo_route
import threading


class Request:
    def __init__(self):
        """
        GET /top250 HTTP/1.1
        Host: movie.douban.com
        Connection: keep-alive

        body
        """
        self.method = 'GET'
        self.headers = {}
        self.path = ''
        self.query = {}
        self.body = ''
        self.cookies = {}

    def add_cookies(self):
        """
        cookies 形式为: a=b; c=d
        """
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=', 1)
                self.cookies[k] = v

    def form(self):
        """
        form 函数用于把 body 解析为一个字典并返回
        body 的格式如下 a=b&c=d&e=1

        可能编码出现: '%E1%E2', 这里需要把 body 里面的数据 unquote 解码
        unquote 可以 unquote('/El%20Ni%C3%B1o/') -> '/El Niño/'
        -> {
            'a': 'b',
            'c': 'd',
            'e': 1,
        }
        """
        args = self.body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[unquote(k)] = unquote(v)
        return f

    def json_parse(self):
        """
        将前端发送的 json 数据转换为一个 python 字典, 数据发送在 body 字段里面
        前端发送的 json 数据格式为:
        '{
            "name": "a"
        }'
        """
        return json.loads(self.body)


def parsed_path(path_with_query):
    """
    path_with_query 是路径, 包括 path 和 query, 如/name?a=1&b=2
    返回为: ('/name', {'a': '1', 'b': '2'})
    """
    u = urlparse(path_with_query)
    path = u.path
    q = parse_qs(u.query)
    query = {k: v[0] for k, v in q.items()}
    return path, query


def parsed_headers(headers):
    """
    "Host: www.douban.com" =>
    {
        "Host": "www.douban.com",
    }
    返回为一组字典
    """
    hs = {}
    header_list = headers.split('\r\n')
    for header in header_list:
        k, v = header.split(': ', 1)
        hs[k] = v
    return hs


def parsed_request(request):
    """
    request 如下
    GET /top250 HTTP/1.1 (header_line)
    Host: movie.douban.com (headers)

    a=1&b=2(body)
    """
    header_line, req = request.split('\r\n', 1)
    headers, body = req.split('\r\n\r\n', 1)
    return header_line, headers, body


def parsed_header_line(header_line):
    method, path, protocol = header_line.split()
    return method, path, protocol


def response_for_path(path, request):
    """
    路由处理函数, 根据 path 的不同调用 routes.py 里面的不同路由函数
    默认为 error

    原理为, 访问一个页面, 就发送了一个 request 请求, 服务器根据请求的路径调用不同的函数
    """
    path, query = parsed_path(path)
    request.path = path
    request.query = query

    # routes 是一个字典, 格式为如下
    routes = {
        # path('/'): 路由函数,
        404: error
    }
    routes.update(route_dict)
    routes.update(todo_route)
    routes.update(weibo_route)
    # 根据 request 的 path 来匹配 routes 里面的 path, 调用 routes 里面的函数
    response = routes.get(path, error)
    return response(request)


def process_request(connection):
    print('连接成功, 使用多线程处理请求', threading.current_thread().name)
    req = connection.recv(1024)
    req = req.decode('utf-8')

    # 防止 Chrome 发送空请求
    if len(req.split()) < 2:
        connection.close()
    header_line, headers, body = parsed_request(req)
    method, path, protocol = parsed_header_line(header_line)
    # 新建一个 request 实例
    request = Request()

    request.method = method
    request.body = body
    request.headers = parsed_headers(headers)
    request.add_cookies()

    response = response_for_path(path, request)
    # 把响应发送给客户端
    connection.sendall(response)
    # 处理完请求, 关闭连接
    connection.close()


def run(host='', port=3000):
    with socket.socket() as s:
        s.bind((host, port))

        while True:
            s.listen(5)
            connection, address = s.accept()

            # 开一个新的线程来处理请求, 第二个参数是传给新函数的参数列表, 必须是 tuple
            t = threading.Thread(target=process_request, args=(connection,))
            t.start()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
