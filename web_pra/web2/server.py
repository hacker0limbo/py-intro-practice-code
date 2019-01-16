import socket


def page(name):
    """
    读取普通文件, 参数为文件名
    """
    with open(name, 'r', encoding='utf-8') as f:
        page = f.read()
        return page


def img(name):
    """
    读取图片文件, 二进制格式
    """
    with open(name, 'rb') as f:
        image = f.read()
        return image


def route_index():
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = page('index.html')
    response = header + '\r\n' + body
    return response.encode('utf-8')


def route_msg():
    """
    msg 页面的处理函数
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Msg</h1>'
    response = header + '\r\n' + body
    return response.encode('utf-8')


def route_image():
    """
    图片的处理函数, 读取图片并生成响应返回
    """
    header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
    body = img('icon.png')
    response = header + b'\r\n' + body
    return response


def error(code=404):
    """
    404 页面处理函数
    """
    response = {
        404: b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nerror'
    }
    return response.get(code, b'')


def response_for_path(path):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404 route
    """
    routes = {
        '/': route_index,
        '/msg': route_msg,
        '/icon.png': route_image,
    }
    response = routes.get(path, error)
    return response()


def run(host='', port=3000):
    """
    启动服务器, socket 进行实例化
    """
    s = socket.socket()
    s.bind((host, port))

    while True:
        s.listen(5)
        connection, address = s.accept()
        request = connection.recv(1024)
        request = request.decode('utf-8')
        path = request.split()[1]

        response = response_for_path(path)
        connection.sendall(response)
        connection.close()


def main():
    config = {
        'host': '',
        'port': 3000,
    }
    run(**config)


if __name__ == '__main__':
    main()
