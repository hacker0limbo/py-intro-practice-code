# RPC 模拟

## 什么是 rpc
远程调用, 两台服务器 A, B, 一个应用部署在 A 服务器上, 需要调用 B 服务器上应用提供的函数和方法, 由于不在一个内存空间, 不能直接调用, 需要通过网络来表达调用的语义和传达调用的数据

## 流程
- 客户端和服务器之间建立 TCP 连接, 远程调用的所有数据都在这个连接里传输.
连接可以是按需连接, 调用结束后就断掉, 也可以是长连接, 多个远程调用共享一个连接
- 寻址, 知道对应服务器的地址, 以及服务器上面的方法名称等
- client stub 将发送数据序列化(以 json 格式发出)到服务端
- 服务器收到请求以后, 将数据反序列化, 恢复成方法然后进行本地调用, 得到返回值, 然后再通过序列化发送到客户端

## 目录结构

```
/client
    clientmain  客户端主文件
    rpcclient   客户端 rpc
    rpcstub     客户端的 rpc stub, 用于将发送数据劫持以后序列化再发送到服务端
    tcpclient   客户端与服务端的连接

/server
    servermain 服务端主文件
    jsondecode  服务端得到数据以后将数据序列化解析为对应方法, 并调用方法
    rpcserver   服务端 rpc
    rpcstub     服务端 rpc stub, 拥有客户端需要调用的方法
    tcpserver   服务端与客户端的连接
```