import socket


class Server:

    def __init__(self):
        """
        服务端连接, 绑定到对应客户端的端口, 建立和客户端的连接
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind_listen(self, port):
        self.s.bind(('0.0.0.0', port))
        self.s.listen(5)

    def accept_receive_close(self):
        (client_socket, address) = self.s.accept()
        # 接受客户端发送的数据, 然后返回给客户端
        msg = client_socket.recv(1024)
        message = self.on_msg(msg)
        client_socket.send(message)
        client_socket.close()