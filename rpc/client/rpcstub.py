import json


class RPCStub:

    def __getattr__(self, item):
        """
        当调用远程方法的时候, rPCSub.foo(a, c=2),
        对发送的方法进行劫持, 使其以 json 序列化的格式
        然后将其发送至服务端
        """
        def _(*args, **kwargs):
            d = {
                'method_name': item,
                'method_args': args,
                'method_kwargs': kwargs
            }
            # 发送数据到服务端
            self.send(json.dumps(d).encode('utf-8'))
        setattr(self, item, _)
        return _
