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