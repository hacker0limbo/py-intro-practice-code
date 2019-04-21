import rpcstub
import tcpclient
import jsondecode


class RPCClient(tcpclient.Client, rpcstub.RPCStub, jsondecode.JsonDecoder):

    def on_msg(self, data):
        self.from_data(data)
        return self.decode_data()
