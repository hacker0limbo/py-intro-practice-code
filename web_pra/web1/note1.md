# 笔记 1

## 使用 https
- https 请求的默认端口是 443
- https 的 socket 连接需要`import ssl`, 并且使用`s = ssl.wrap_socket(socket.socket())`来初始化

## HTTP 协议的 301 状态
请求如下地址:
http://movie.douban.com/top250
返回结果是一个 301
301 状态会在 HTTP 响应头的 Location 部分告诉你应该转向的 URL
所以, 如果遇到 301, 就请求新地址并且返回

响应如下:
```
HTTP/1.1 301 Moved Permanently
Date: Sun, 13 Jan 2019 12:04:54 GMT
Content-Type: text/html
Location: https://movie.douban.com/top250
Server: dae
X-Content-Type-Options: nosniff
```

## 端口
http 默认端口是 80, https 默认端口是 443, 因此在发生请求的时候根据协议设置不同的端口

