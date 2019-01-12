# coding: utf-8

import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s = socket.socket()
# s = ssl.wrap_socket(socket.socket())
host = 'g.cn'
port = 80
s.connect((host, port))
ip, port = s.getsockname()

print('本机 ip 和 port {} {}'.format(ip, port))

http_request = 'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)
request = http_request.encode('utf-8')

print('请求', request)

s.send(request)
response = s.recv(1023)

print('响应', response)
print('响应的 str 格式', response.decode('utf-8'))
