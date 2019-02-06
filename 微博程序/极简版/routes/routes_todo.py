from models.todo import Todo
from routes import j_template, response_with_headers, redirect, error
from routes.routes import current_user, login_required, current_u
from models.user import User


@login_required
def todo_index(request):
    """
    todo 首页函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    # 找到当前登录的用户, 如果没有登录, 就 redirect 到 /login
    u = current_u(request)

    todos = Todo.find_all(user_id=u.id)
    body = j_template('todo_index.html', todos=todos)
    header = response_with_headers(headers)
    response = header + '\r\n' + body
    return response.encode('utf-8')


@login_required
def todo_add(request):
    """
    用于增加 todo 的路由函数
    """
    u = current_u(request)
    u_id = u.id
    if request.method == 'POST':
        form = request.form()
        form.update({
            'user_id': u_id
        })
        t = Todo(form)
        Todo.add(t)
    return redirect('/todo')


@login_required
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
    body = j_template('todo_edit.html')
    body = body.replace('{{todo_id}}', str(t.id))
    body = body.replace('{{todo_title}}', str(t.title))

    header = response_with_headers(headers)
    response = header + '\r\n' + body
    return response.encode('utf-8')


@login_required
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
    '/todo': todo_index,
    '/todo/add': todo_add,
    '/todo/edit': todo_edit,
    '/todo/update': todo_update,
    '/todo/delete': todo_delete,
}

