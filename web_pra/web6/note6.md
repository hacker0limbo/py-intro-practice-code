# Jinja 模板

该课使用 jinja 改写之前的 todo, 整理为一个单独的项目, 地址为: https://github.com/hacker0limbo/todo/tree/master/todo/todo-V4.5.0-jinja

## jinja 笔记

jinja 可以使用`.`来访问一个字典的 value 或者一个对象的属性

变量可以直接调用一个函数, 比如:
```jinja2
name: {% u.get_name() if u.age > 18 and u %}
```

