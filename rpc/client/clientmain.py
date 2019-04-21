import rpcclient


if __name__ == '__main__':
    client = rpcclient.RPCClient()
    client.connect('127.0.0.1', 6000)
    # 调用远程发方法
    client.bar(1, 2, c=3)
    data = client.receive()
    print(client.on_msg(data))
   