"""
py3 中, bytes 和 str 的互相转换是
str.encode('utf-8')
bytes.decode('utf-8')

send 函数和 recv 函数返回值都是 bytes 类型
"""
import socket


def protocol_of_url(url: str):
    """
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    如果没有指定, 默认隐藏了 'http'
    返回代表协议的字符串, 'http' 或者 'https'
    """
    if 'http' in url:
        protocol =  url.split('://')[0]
    else:
        protocol = 'http'
    return protocol


def host_of_url(url: str):
    """
    url 为字符串, 可能值为:
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'
    'http://g.cn:3000/search'

    返回代表主机的字符串, 比如 'g.cn'
    """
    if 'http' in url:
        path = url.split('://')[1]
    else:
        path = url[:]
    if '/' in path and ':' not in path:
        host = path.split('/')[0]
    elif ':' in path:
        host = path.split(':')[0]
    else:
        host = path[:]
    return host


def port_of_url(url: str):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'
    'http://g.cn:3000/search'

    返回代表端口的数字, 比如 80 或者 3000
    80 是 http 默认端口
    443 是 https 默认端口
    '''
    if 'http' in url:
        path = url.split('://')[1]
        if ':' not in path:
            if url[:5] == 'http:':
                return 80
            if url[:5] == 'https':
                return 443
    else:
        path = url[:]
    if ':' in path:
        path_with_host = path.split(':')[1]
        if '/' in path_with_host:
            port = path_with_host.split('/')[0]
        else:
            port = path_with_host[:]
    else:
        port = '80'
    return int(port)


def path_of_url(url: str):
    """
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'
    'http://g.cn:3000/search'

    返回路径, 只要 g.cn:3000/search 返回 '/search'
            其他默认为 '/'
    """
    if 'http' in url:
        paths = url.split('://')[1]
    else:
        paths = url[:]
    if '/' in paths :
        if paths.split('/', 1)[1] == '':
            path = '/'
        else:
            path = '/' + paths.split('/', 1)[1]
    else:
        path = '/'
    return path


def parsed_url(url: str):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回一个 tuple, 内容如下 (protocol, host, port, path)
    '''
    protocol = protocol_of_url(url)
    host = host_of_url(url)
    port = port_of_url(url)
    path = path_of_url(url)
    return protocol, host, port, path


def get(url: str):
    """
    使用 socket 连接服务器, 获得数据并返回
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    protocol, host, port, path = parsed_url(url)
    print(host, port)
    s.connect((host, port))
    # host 一定要写
    http_request = 'GET {} HTTP/1.1\r\nhost:{}\r\nConnection: close\r\n\r\n'.format(path, host)
    req = http_request.encode('utf-8')
    s.send(req)

    data = ''
    while True:
        res = s.recv(1024).decode('utf-8')
        data += res
        if len(res) < 1024:
            break
    s.close()
    return data


def parsed_response(r: str):
    """
    把得到的 response 解析出来
    返回 状态码(int), headers(dict), body(str)

    res 格式如下:
    HTTP/1.1 200 OK (响应部分)
    Date: Sun, 13 Jan 2019 12:05:29 GMT (headers 开始)
    Content-Type: text/html; charset=utf-8

    body
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
