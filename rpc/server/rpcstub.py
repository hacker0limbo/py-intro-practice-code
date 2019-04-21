class RPCStub:
    def __init__(self):
        """
        服务端定义了一些远程方法
        """
        pass

    def foo(self, a, b, c):
        print('foo')
        return (a, b, c)

    def bar(self, a, b, c=10):
        print('bar')
        return (a, b, c)