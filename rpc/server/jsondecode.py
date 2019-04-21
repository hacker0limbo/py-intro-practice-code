import json


class JsonRPC:
    def __init__(self):
        """
        将客户端得到的数据反序列化, 解析成真正的方法
        """
        self.data = None

    def from_data(self, data):
        self.data = json.loads(data.decode('utf-8'))

    def call_method(self):
        method_name = self.data['method_name']
        method_args = self.data['method_args']
        method_kwargs = self.data['method_kwargs']

        return getattr(self, method_name)(*method_args, **method_kwargs)

    def send_data(self, data):
        return json.dumps(data).encode('utf-8')