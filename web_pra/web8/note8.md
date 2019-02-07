# 数据库的使用

基本操作: 

**CRUD**
1. 增加数据(create)
2. 删除数据(delete)
3. 修改数据(update)
4. 查询数据(retrieve)

## sqlite

### cursor
数据库里面的`cursor`用来遍历数据库记录的控制结构, 可以检索, 插入和删除数据, 一个游标为指向一组数据的指针.
`cursor`通常可以代表最后 fetch 到的结果

当执行一条语句的时候可以使用`cursor.execute()`或者`conn.execute()`. 两者区别在于前者会得到返回的 cursor 数据. 而对于`insert`, `delete`, `update`往往不需要得到数据,
因此可以直接使用后者操作, 对于`select`需要返回结果, 往往使用前者(cursor)


### 基本使用:

```python
import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

sql = """
xxx
"""

cursor.execute(sql)
cursor.rowcount 
values = cursor.fetchall() # [('1', 'abc')]
cursor.close()

conn.commit() # 提交事务
conn.close()
```

参数:
参数通过`?`来占位, 参数按照位置传递给`execute()`方法, 例如:
```python
cursor.execute('select * from user where name=? and pwd=?', ('abc', 'password'))
```

关于`cursor`对象执行不同的语句:
- `insert`，`update`，`delete`: 执行结果由`rowcount`返回影响的行数，就可以拿到执行结果
- `select`: 通过`featchall()`可以拿到结果集。结果集是一个`list`，每个元素都是一个`tuple`，对应一行记录

### 几个 api
`cursor.description`: 返回一个 tuple, 里面包含子 tuple, 每个子 tuple 的第一个元素对应一个 column 名, 如:
```python
# 假设该表只有两个 column, id 和 username
(('id', None, None, None, None, None, None), ('username', None, None, None, None, None, None))
```

`row_factory(cursor, row)`: row 为对应数据库里面的一条数据, 可以对该函数重新赋值来得到不同格式的数据, 比如下面的例子可以得到字典形式:
```python
import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

con = sqlite3.connect(":memory:")
con.row_factory = dict_factory
cur = con.cursor()
cur.execute("select 1 as a")
print(cur.fetchone()) # {'a': 1}

```

## 几个概念

使用`with`语句自动提交`commit`修改, 实例如下:
```python
conn = sqlite3.connect(db_filename)

with conn:
    cur = conn.cursor()
    cur.execute( ... )
```

- connection object 连接对象可以被用来作为 context managers, 能够自动提交(commit)和回滚(rollback)事务, 报错就rollback, 否则commit
  对于 DELETE, UPDATE, INSERT 比较有效
- 在 context manager 里面连接不会自动关闭, 除非使用`conn.commit()`手动关闭
- `with`语句不会创造一个新的作用域, 因此 with 里面定义的变量, with 外面还是可以使用
- `conn`直接连接一次就行, 也不用关闭, 如果有多个 module 要用到这个连接就需要使用 ORM 了.

## sql 注入

用户可以在发送的数据里面伪造 sql 拼接字符串注入到代码里面, 典型的比如不使用`?`作为占位符, 比如:

登录需要输入账号和密码, 输入以后表单提交到服务器, 用 select 语句查询数据库里面是否存在这样的用户, 如果 select 语句如下

```python
def select(conn, form):
    cursor = conn.cursor()
    uname = form.get('username', '')
    pwd = form.get('password', '')
    sql = """
    SELECT 
        *
    FROM
        User
    WHERE
        username="{}" and password="{}"
    """.format(uname, pwd)

    cursor.execuate(sql)
    return cursor.fetchall()
```

假设以上代码, 用户提交的数据为:

```python
form = {
    'username': 'bobo" or "1"="1'
    'password' = ''
}
```
那么 sql 语句就变成了`Where username="bobo" or "1"="1" and password=""`, 这里 username 是正确的情况下该语句恒成立(先执行 and 再执行 or), 所以可以不用输入密码就登录.

## 技巧

对于测试数据库, 可以在测试开始的时候(`setUp`)建立一个数据库, 在结束的时候删除该数据库(`tearDwon`)

## Reference
- https://stackoverflow.com/questions/6318126/why-do-you-need-to-create-a-cursor-when-querying-a-sqlite-database
- https://stackoverflow.com/questions/19522505/using-sqlite3-in-python-with-with-keyword
- https://stackoverflow.com/questions/9561832/what-if-i-dont-close-the-database-connection-in-python-sqlite
- https://stackoverflow.com/questions/4610791/can-i-put-my-sqlite-connection-and-cursor-in-a-function
- https://stackoverflow.com/questions/2330344/in-python-with-sqlite-is-it-necessary-to-close-a-cursor