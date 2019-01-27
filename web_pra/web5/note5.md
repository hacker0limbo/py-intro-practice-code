# Todo 程序

## 路由函数

路由函数是根据 path 来调用不同的路由函数的, 注意这里的 path 不包含 query, 在路由函数里面再进行 query 的细化.

因此, 假设请求`'/todo/delete?id=1'`, 调用的是`/delete`的路由函数, 然后在这个函数里面判断`query`, 得到相应的`id`对应`todo`

## todo 流程

点击添加按钮增加一个新的 todo 的时候, 程序的流程如下(包含原始 HTTP 报文)

1. 浏览器提交一个表单给服务器(发送 POST 请求)
```
POST /todo/add HTTP/1.1
Content-Type: application/x-www-form-urlencoded

title=heuv
```

2. 服务器解析出表单的数据, 并且增加一条新数据, 并返回 302 响应
```
HTTP/1.1 302 REDIRECT
Location: /todo
```

3. 浏览器根据 302 中的地址, 自动发送了一条新的 GET 请求
```
GET /todo HTTP/1.1
Host: ....
```

4. 服务器给浏览器一个页面响应
```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: ...

<html>
    ....
</html>
```

5. 浏览器把新的页面显示出来

