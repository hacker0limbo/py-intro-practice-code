import rpcserver


if __name__ == '__main__':
    server = rpcserver.RPCServer()
    server.loop()