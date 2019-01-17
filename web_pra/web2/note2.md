# web2 笔记

## open 方法
`open()` 方法用于打开一个文件，并返回文件对象

`open(file, mode='r', buffering=-1, encoding=None)`

其中, mode 可以是`r`, `w`, `rb`(二进制打开, 一般用于读取图片, 读取内容返回也是二进制)

## *args 和 **kwargs

要传入不定的参数, 可以这样:
```python
# 直接传
n = (1, 2, 3)
m = {'a':1, 'b':2}

fn(1, 2, 3)
fn(a=1, b=2)

# 用 *args
fn(*n)

# 用 **kwargs
# 其中, a, b 就是变量了, 直接在函数里面可以用的
fn(**m)

# 例子:
def f(a, b):
    print(a + b)

n = (1, 3)
m = {'a':1, 'b':2}
f(*n) # 4
f(**m) # 3
```

## 表单验证

### html
```html
<form action="/" method="get">
    <label for="user"></label>
    <input name="user" id="user" value="">
    <button type="submit"></button>
</form>
```
action 表示发送以后发送新的请求的路径, method 表示方法

### get 和 post
使用 get 方法发送的数据附在了请求的 url 里面, 如上请求的 url 为: `/?user=xxx`

使用 post 方法发送的数据在 body 里面, 如上为: `user=xxx`

点击了 button 都会发送一个新的请求, 请求里面就有发送的数据, 所以页面可能刷新或者前往新的页面, 因此可以在 js 里面用 `e.prevenDefault()` 来阻止页面刷新