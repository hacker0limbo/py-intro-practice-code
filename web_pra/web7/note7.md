# 摘要算法, 盐, 索引

## 摘要算法
给定任意长度的一段数据可以生成定长的密文, 摘要结果不可逆, 不能被还原为原数据

- 摘要不是加密, 摘要是不可逆的
- 数据库里面一般不存明文密码, 所以一般无法修改密码, 只能重置密码
- 两个极为相似的数据生成的密文一般相差很远, 一般两个不同的数据是无法产生相同的结果的(无碰撞)
- 单向性, 不可逆. 即不同的数据输入一定是不同的密文, 相同的数据输入一定是相同的密文
- 课用来加密用户密码或者做数据完整性验证(比如网站在下载页面公布文件的 sha1 摘要结果, 你下载后自己生成结果来对比, 就能知道文件是否被篡改)

常见的算法有`md5`和`sha1`

用法:

```python
import hashlib
# 要加密的是 'abc'
# 用 ascii 编码转换成 bytes 对象
pwd = 'abc'.encode('ascii')
# 创建 md5 对象
m = hashlib.md5(pwd)
# 返回摘要字符串
print(m.hexdigest())
#
# 创建 sha1 对象
s = hashlib.sha1(pwd)
# 返回摘要字符串
print(s.hexdigest())
```

## 彩虹表
一张表可以对加密的结果进行反向查询, 如果知道了算法类型和最后的密文可以通过暴力破解方法进行匹配, 当然仅限简单摘要后的密码

```python
# pwd 是一段(000~999)加密以后的密文
pwd = 203xxxxxxxx
for i in range(0, 1000):
    p = str(i).zfill(3)
    b = p.encode('ascii')
    password = hashlib.sha256(b).hexdigest()
    if password == pwd:
        print(p)
        break
```

## 带盐密码
对密码再额外加上额外的信息后进行摘要算法, 比如这样`sha256(password + xxx)`, `xxx`就是盐(salt)
注意, 每一个用户可以都使用相同的盐值

这样, 无法通过彩虹表来查询这个到原始密码

## 索引

原始数据如下, 要查找 id 为 n 的元素的 pwd 需要 n * 3
```json
[
    {
        "id": 1,
        "name": "a",
        "pwd": 123
    },
    {
        "id": 1,
        "name": "a",
        "pwd": 123
    }
]
```

修改1, 改用字典形式:

```json
{
  "1": {
    "id": 1,
    "name": "a",
    "pwd": 123
  }, 
  "2": {
    "id": 2,
    "name": "b",
    "pwd": 456
  }
}
```

要求通过一个字段(username)来查找数据, 这时需要对这个字段建立索引 

```json
{
  "index": {
    "username": {
      "a": 1,
      "b": 2
    }
  },
  "data": [
      {
        "id": 1,
        "name": "a",
        "pwd": 123
      }, 
      {
        "id": 2,
        "name": "b",
        "pwd": 456
      }
  ]
}
```

## 微博

## 基本思路

- 所有的用户即使没有登录也可以访问 `/weibo/index?id=1` 来查看每个用户的微博, 当无权对任何用户的, 所以 index 页面没有使用`login_required()`


### model
- user
- weibo
- comment

关系: 
- 一个 user 多个 weibo
- 一个 user 多个 comment
- 一个 weibo 多个 comment

存取方法: 
- 每个 weibo 存 user_id
- 每个 comment 存 user_id
- 每个 comment 存 weibo_id
