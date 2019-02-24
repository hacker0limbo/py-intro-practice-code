# note15

session 和 cookie, 留言版和微博套路

## flask-sqlalchemy

声明一个基类需要如下:

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr

db = SQLAlchemy()

class Model(db.Model):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'

"""
__abstrat__ 表明该类不会被创建, 作为虚拟使用
@declared_attr 可以声明表的属性, 比如这里声明表的名字为 小写的类名+s
"""
```

## 动态路由在模板里面需要传递参数的时候如下:
```jinja2
<a href={{ url_for('message.delete', message_id=m.id) }}>删除评论</a>
<!-- 其中 message_id 为路由函数参数, m.id 为传入的值 -->
```

## session 和 cookie

session 比 cookie 更加安全, 使用 session

1. cookie 存储在客户端, 不安全, 可以伪造, 比如最原始的如下:
    cookie = { 'username': 'a' }
2. 之前的 session 配合 cookie 一起使用, 如下:
    session_id 是一个随机字符串
    cookie = { 'username': 'session_id' }
    session = { 'session_id': 'a' }
    通过 session_id 中间接口获得用户
3. flask 里面直接使用 app.secret_key 进行 session 的加密, 然后直接使用 session['username'] = 'a' 设置 session

登录和登出:
登录: 增加 session, 记录状态
登出: 删除 session, session.pop() 消除状态


### 如何设置

在视图函数里面设置 cookie 的时候, 由于视图函数返回一个相应对象, 如果返回的是一个字符串(比如使用 redner_template() 函数), 
会根据这个字符串生成一个相应对象
相应对象包含 headers, 响应头, 响应体, 所以使用 cookie 的时候, 需要先使用 make_response 构造响应体, 再对该相应设置 cookie

