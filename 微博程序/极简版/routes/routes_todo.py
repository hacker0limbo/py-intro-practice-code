from models.todo import Todo
from routes import template, response_with_headers, redirect, error
from routes.routes import current_user, login_required
from models.user import User


def todo_index(request):
    """
    todo 首页函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    # 找到当前登录的用户, 如果没有登录, 就 redirect 到 /login
    username = current_user(request)
    u = User.find_by(username=username)

    todo_list = Todo.find_all(user_id=u.id)
    # 生成 todo list 的 HTML 字段
    todos = []
    for i, t in enumerate(todo_list):
        # 第几个 task 直接用 index 来定位, 不需要新建一个 task_id 来存储
        edit_link = f'<a href="/todo/edit?id={t.id}">编辑</a>'
        delete_link = f'<a href="/todo/delete?id={t.id}">删除</a>'
        s = f'<h3>{i+1} : {t.title} {edit_link} {delete_link}</h3>'
        todos.append(s)
    todo_html = ''.join(todos)
    body = template('todo_index.html')
    body = body.replace('{{todos}}', todo_html)

    header = response_with_headers(headers)
    response = header + '\r\n' + body
    return response.encode('utf-8')


def todo_add(request):
    """
    用于增加 todo 的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    username = current_user(request)
    u = User.find_by(username=username)

    if request.method == 'POST':
        form = request.form()
        t = Todo(form)
        todos = Todo.find_all(user_id=u.id)
        Todo.add(t, u.id)
    # 客户端发送了数据服务器处理完毕以后, 数据被写入数据库
    # 重定向到 /todo 页面, 相当于刷新页面, 重新发送 请求到 todo 页面, 然后该页面的路由处理
    # 先 post 到了 /todo/add, 然后 302 重定向到 /todo
    # redirect 保证了 只在 /todo 页面查看数据
    return redirect('/todo')


def todo_edit(request):
    """
    编辑页面显示
    """
    headers = {
        'Content-Type': 'text/html',
    }
    username = current_user(request)
    u = User.find_by(username=username)
    # 得到当前编辑的 todo 的 id
    # 此时页面的 url 含有 query ?id=1, request.query 解析为了一个字典
    todo_id = request.query.get('id', -1)
    if todo_id == -1:
        # 没找到, 反正错误页面
        return error(request)
    t = Todo.find_by(id=int(todo_id))
    if t.user_id != u.id:
        # 如果 todo 的 user_id 不是 对应的 user 的 id, 无法修改该 todo
        return redirect('/login')
    body = template('todo_edit.html')
    body = body.replace('{{todo_id}}', str(t.id))
    body = body.replace('{{todo_title}}', str(t.title))

    header = response_with_headers(headers)
    response = header + '\r\n' + body
    return response.encode('utf-8')


def todo_update(request):
    """
    修改 todo 的路由, todo_edit 页面表单发送的数据在这个路由处理
    """
    form = request.form()
    todo_id = int(form.get('id', -1))
    todo_title = form.get('title', '')
    Todo.update(todo_id, todo_title)
    return redirect('/todo')


def todo_delete(request):
    username = current_user(request)
    u = User.find_by(username=username)
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        # 如果 todo 的 user_id 不是 对应的 user 的 id, 无法删除该 todo
        return redirect('/login')

    Todo.remove(todo_id)
    return redirect('/todo')


route_dict = {
    '/todo': login_required(todo_index),
    '/todo/add': login_required(todo_add),
    '/todo/edit': login_required(todo_edit),
    '/todo/update': login_required(todo_update),
    '/todo/delete': login_required(todo_delete),
}

