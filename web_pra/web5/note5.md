# Todo 程序

## 路由函数

路由函数是根据 path 来调用不同的路由函数的, 注意这里的 path 不包含 query, 在路由函数里面再进行 query 的细化.

因此, 假设请求`'/todo/delete?id=1'`, 调用的是`/delete`的路由函数, 然后在这个函数里面判断`query`, 得到相应的`id`对应`todo`



