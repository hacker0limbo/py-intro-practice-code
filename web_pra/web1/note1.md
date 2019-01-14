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

### 301 与 302
301 redirect(重定向): 永久性转移(Permanently moved)
302 redirect(重定向): 代表行转移(Temporarily Moved)

301 与 302 都代表重定向, 浏览器在拿到服务器返回的这个状态码后自动跳转到一个新的 URL 地址, 该地址从响应的 Location 字段获取.
不同在于: 
- 301 表示旧地址的资源已经被永久地移除了(这个资源不可访问了), 搜索引擎在抓取新内容的同时也将旧的网址交换为重定向之后的网址
- 302 表示旧地址还可以访问, 搜索引擎会抓取新的内容而保存旧的网址

301 常用的是做域名的跳转 比如 <http://veryyoung.github.io> 会重定向到 <http://veryyoung.me>
302 临时跳转, 比如未登陆的用户访问用户中心重定向到登陆页面. 访问 404 页面会自动重定向到首页

### 302 劫持
收到 302 时重定向到新的网站抓取页面的时候 目标网址错误, 跑到了别的网站去抓取了页面, 比如被劫持到了 博彩网址, [案例](https://www.v2ex.com/t/465489)

## 端口
http 默认端口是 80, https 默认端口是 443, 因此在发生请求的时候根据协议设置不同的端口

## Reference
- http://tool.chinaz.com/pagestatus/ http 状态查询