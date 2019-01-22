# 笔记 session 和 cookie
服务器可以返回响应, 里面包含`Set-Cookie`字段, 浏览器接受响应以后会保存这个字段里面数据, 以后每次再访问这个页面会在请求里面加上`cookie`字段发送到服务器.

## cookie 
用来个人信息, 由于 http 协议的无状态性, 发送请求以后服务器并不知道是哪个用户发送的, 因此可以在 cookie 里面添加用户个人信息进行判断
同时, 不同的用户有不同的状态, 比如登录与未登录

cookie 是存在浏览器里面的, 因此可以实现一些功能, 比如自动登录

同时一些网站还会出现比如: 账号过期, 然后你被自动登出, 这是由于 cookie 过期, expire 设置了时间

cookie 格式为: `cookie: a=b; c=d`

### 用户(session)
session 是加密了的 cookie, 假设没有 session, 那么发出的 cookie 很容易伪造, 比如就是`cookie: user=a`, 那么任何人都可以像服务器发出这么一个请求(比如直接使用 request 库发送)来伪造成用户 a, 服务器接受请求解析 a 的个人信息就暴露了.
session 可以让 cookie 里面的数据不容易伪造, 比如可以是一段复杂的字符串(`token`), 服务器得到数据以后根据这个令牌来得到原始数据

```python
# 客户端的 cookie
cookie = {
    'username': 'abc123qwe'
}

# 服务端的 session
session = {
    'abc123qwe': 'gw'
}

# abc123qwe 就是令牌
```

第一次登陆, 浏览器发送给服务器的请求包含了账号和密码, 服务器得到账号密码以后返回的响应里面设置 `Set-Cookie` 字段, 可以在浏览器设置针对该域名的 cookie, 如下

request header 里面设置为`cookie: user: secret_id`, secret_id 是一段加密的字符串, 如果直接使用用户名容易被人伪造. 发送了 cookie 到服务器以后, 服务器有`session`来 
进行验证, 形式为字典: `{secret_id: [username]}`, username 保存了用户的信息 

以后再次访问登录页面, 发送了一个 Get 请求, 里面包含了 cookie 字段, 服务器验证以后直接渲染页面, 不用再填写表单发送 Post 请求了

### 存储 session 持久化
1. 保存到文件
2. 对称加密, cookie 里面存取的数据就是原始数据, 但是是经过服务器特定加密算法加密的, 服务器得到以后再解密就直接得到原始数据 


## 301 重定向 cache 问题
浏览器会缓存 301 的 http request, 因此需要清除 cache, 方法为: https://superuser.com/questions/304589/how-can-i-make-chrome-stop-caching-redirects

## 修改密码问题

由于可能存在别人拿到你的 cookie 进行密码修改, 因此现在很多网站改密码都要求输入原密码, 这样让你即使知道了 cookie 也是无法知道密码, 
需要经过 session 解析才能得到密码. 因此即使别人拿了你的 cookie 也可能只能登陆你的界面看看你的个人信息, 无法修改密码

## 公共 wifi
问题: ARP 欺骗
解决办法: https