import socket

host = ''
port = 2000

s = socket.socket()
s.bind((host, port))


while True:
    s.listen(5)
    connection, address = s.accept()

    request = connection.recv(1024)

    print('ip and request, {}\n{}'.format(address, request.decode('utf-8')))

    response = b'<h1>Hello World!</h1>'
    connection.sendall(response)
    connection.close()
