import socket


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.s.connect((host, port))

    def send(self, data):
        self.s.send(data)

    def receive(self):
        return self.s.recv(1024)

    def close(self):
        self.s.close()