import socket

# '' 表示接受接受任意 ip 地址的连接, 若为 127.0.0.1 表示本机
host = ''
port = 2000

s = socket.socket()
s.bind((host, port))

while True:
    s.listen(5)
    # 连接, 客户端 ip 地址
    connection, address = s.accept()
    request = connection.recv(1024)
    print(request.decode('utf-8'))

    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello</h1>'
    response = header + '\r\n' + body

    connection.sendall(response.encode('utf-8'))
    connection.close()

"""
访问 localhost:2000

打印出来的 request 如下:

GET / HTTP/1.1
Host: localhost:2000
Connection: keep-alive
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7
Cookie: xxx
"""