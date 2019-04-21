import json


class JsonDecoder:
    def __init__(self):
        """
        将服务端户端得到的数据反序列化, 解析成真正的方法
        """
        self.data = None

    def from_data(self, data):
        self.data = json.loads(data.decode('utf-8'))

    def decode_data(self):
        return tuple(self.data)
