import socket
import ssl


"""
作业 1 答案
===

"""
def parsed_url(url):
    """
    解析 url 返回 (protocol host port path)
    有的时候有的函数, 它本身就美不起来, 你要做的就是老老实实写
    """
    # 检查协议
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        # '://' 定位 然后取第一个 / 的位置来切片
        u = url

    # https://g.cn:1234/hello
    # u 为 g.cn:1234/hello

    # 检查默认 path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # 检查端口
    port_dict = {
        'http': 80,
        'https': 443,
    }
    # 默认端口
    port = port_dict[protocol]
    # if host.find(':') != -1:
    if ':' in host:
        h = host.split(':')
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path


def socket_by_protocol(protocol):
    """
    根据协议返回一个 socket 实例
    """
    if protocol == 'http':
        s = socket.socket()
    else:
        # HTTPS 协议需要使用 ssl.wrap_socket 包装一下原始的 socket
        # 除此之外无其他差别
        s = ssl.wrap_socket(socket.socket())
    return s


def response_by_socket(s):
    """
    参数是一个 socket 实例
    返回这个 socket 读取的所有数据
    """
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r
    return response


def parsed_response(r):
    """
    把 response 解析出 状态码 headers body 返回
    状态码是 int
    headers 是 dict
    body 是 str
    """
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v
    return status_code, headers, body


def get(url):
    """
    用 GET 请求 url 并返回响应
    """
    protocol, host, port, path = parsed_url(url)
    s = socket_by_protocol(protocol)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = response_by_socket(s)
    print('get response, ', response)
    r = response.decode(encoding)

    status_code, headers, body = parsed_response(r)
    if status_code in [301, 302]:
        url = headers['Location']
        return get(url)

    return status_code, headers, body


def main():
    url = 'http://movie.douban.com/top250'
    status_code, headers, body = get(url)
    print('main', status_code)
    # print('main headers ({})'.format(headers))
    # print('main body', body)

# 以下 test 开头的函数是单元测试
def test_parsed_url():
    """
    parsed_url 函数很容易出错, 所以我们写测试函数来运行看检测是否正确运行
    """
    http = 'http'
    https = 'https'
    host = 'g.cn'
    path = '/'
    test_items = [
        ('http://g.cn', (http, host, 80, path)),
        ('http://g.cn/', (http, host, 80, path)),
        ('http://g.cn:90', (http, host, 90, path)),
        ('http://g.cn:90/', (http, host, 90, path)),
        #
        ('https://g.cn', (https, host, 443, path)),
        ('https://g.cn:233/', (https, host, 233, path)),
    ]
    for t in test_items:
        url, expected = t
        u = parsed_url(url)
        # assert 是一个语句, 名字叫 断言
        # 如果断言成功, 条件成立, 则通过测试
        # 否则为测试失败, 中断程序报错
        e = "parsed_url ERROR, ({}) ({}) ({})".format(url, u, expected)
        assert u == expected, e


def test_parsed_response():
    """
    测试是否能正确解析响应
    """
    # NOTE, 行末的 \ 表示连接多行字符串
    response = 'HTTP/1.1 301 Moved Permanently\r\n' \
        'Content-Type: text/html\r\n' \
        'Location: https://movie.douban.com/top250\r\n' \
        'Content-Length: 178\r\n\r\n' \
        'test body'
    status_code, header, body = parsed_response(response)
    assert status_code == 301
    assert len(list(header.keys())) == 3
    assert body == 'test body'


def test_get():
    """
    测试是否能正确处理 HTTP 和 HTTPS
    """
    urls = [
        'http://movie.douban.com/top250',
        'https://movie.douban.com/top250',
    ]
    # 这里就直接调用了 get 如果出错就会挂, 测试得比较简单
    for u in urls:
        get(u)


def test():
    """
    用于测试的主函数
    """
    test_parsed_url()
    # test_get()
    # test_parsed_response()


if __name__ == '__main__':
    # test()
    main()

