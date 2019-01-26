from models.todo import Todo
from routes import template, response_with_headers, redirect, error


def todo_index(request):
    """
    todo 首页函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    todo_list = Todo.all()
    # 生成 todo list 的 HTML 字段
    # todo_html = ''.join([f'<h3>{t.id} : {t.title}</h3>' for t in todo_list])
    todos = []
    for t in todo_list:
        edit_link = f'<a href="/todo/edit?id={t.id}">编辑</a>'
        delete_link = f'<a href="/todo/delete?id={t.id}">删除</a>'
        s = f'<h3>{t.id} : {t.title} {edit_link} {delete_link}</h3>'
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
    if request.method == 'POST':
        form = request.form()
        t = Todo(form)
        Todo.add(t)
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
    # 得到当前编辑的 todo 的 id
    # 此时页面的 url 含有 query ?id=1, request.query 解析为了一个字典
    todo_id = request.query.get('id', -1)
    if todo_id == -1:
        # 没找到, 反正错误页面
        return error(request)
    t = Todo.find_by(id=int(todo_id))
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
    todo_id = int(request.query.get('id', -1))
    Todo.remove(todo_id)
    return redirect('/todo')


route_dict = {
    '/todo': todo_index,
    '/todo/add': todo_add,
    '/todo/edit': todo_edit,
    '/todo/update': todo_update,
    '/todo/delete': todo_delete,
}

