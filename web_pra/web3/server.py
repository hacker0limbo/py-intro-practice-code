import socket
from urllib.parse import urlparse, unquote, parse_qs
from routes.routes import route_dict, error

class Request:
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''

    def form(self):
        """
        form 函数用于把 body 解析为一个字典并返回
        body 的格式如下 a=b&c=d&e=1
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
            f[unquote(k)] = v
        return f


request = Request()


def parsed_path(path):
    """
    path 是路径, 包括 path 和 query, 如/name?a=1&b=2
    返回为: ('/name', {'a': '1', 'b': '2'})
    """
    u = urlparse(path)
    path = u.path
    q = parse_qs(u.query)
    query = {k: v[0] for k, v in q.items()}
    return path, query


def response_for_path(path):
    """
    路由处理函数, 根据 path 的不同调用 routes.py 里面的不同路由函数
    默认为 error
    """
    path, query = parsed_path(path)
    request.path = path
    request.query = query

    routes = {
    }
    routes.update(route_dict)
    response = routes.get(path, error)
    return response(request)


def run(host='', port=5000):
    with socket.socket() as s:
        s.bind((host, port))

        while True:
            s.listen(5)
            connection, address = s.accept()
            # 接受请求
            req = connection.recv(1024)
            req = req.decode('utf-8')

            # 防止 Chrome 发送空请求
            if len(req.split()) < 2:
                continue
            path = req.split()[1]
            request.method = req.split()[0]
            request.body = req.split('\r\n\r\n', 1)[1]

            response = response_for_path(path)
            # 把响应发送给客户端
            connection.sendall(response)
            # 处理完请求, 关闭连接
            connection.close()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
