import tcpserver
import rpcstub
import jsondecode


class RPCServer(tcpserver.Server, jsondecode.JsonRPC, rpcstub.RPCStub):
    def __init__(self):
        super(RPCServer, self).__init__()

    def loop(self):
        self.bind_listen(6000)
        while True:
            self.accept_receive_close()

    def on_msg(self, data):
        # 得到数据, 反序列化
        self.from_data(data)
        # 将反序列化的数据解析为方法并调用, 返回给客户端
        send_data = self.call_method()
        return self.send_data(send_data)