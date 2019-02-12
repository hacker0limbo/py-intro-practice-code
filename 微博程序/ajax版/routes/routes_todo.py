from models.todo import Todo
from routes import j_template, redirect, error, http_response
from routes.routes import login_required, current_u


def current_required(route_function):
    """
    当前用户只对当前的 todo 有操作权限, 否则前往 login 页面
    """
    def func(request):
        u = current_u(request)
        todo_id = int(request.query.get('id', -1))
        t = Todo.find_by(id=todo_id)
        if t.user_id != u.id:
            # 如果 todo 的 user_id 不是 对应的 user 的 id, 无法对 todo 操作
            return redirect('/login')
        else:
            # 登录了, 正常返回路由函数响应
            return route_function(request)
    return func


@login_required
def todo_index(request):
    """
    todo 首页函数
    """

    # 找到当前登录的用户, 如果没有登录, 就 redirect 到 /login
    u = current_u(request)

    todos = Todo.find_all(user_id=u.id)
    body = j_template('todo_index.html', todos=todos)
    return http_response(body)


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
@current_required
def todo_edit(request):
    """
    编辑页面显示
    """
    todo_id = request.query.get('id', -1)
    if todo_id == -1:
        # 没找到, 返回错误页面
        return error(request)
    t = Todo.find_by(id=int(todo_id))
    body = j_template('todo_edit.html', todo=t)
    return http_response(body)


@login_required
def todo_update(request):
    """
    修改 todo 的路由, todo_edit 页面表单发送的数据在这个路由处理
    """
    form = request.form()
    todo_id = int(form.get('id', -1))
    todo_title = form.get('title', '')
    Todo.update(todo_id, title=todo_title)
    return redirect('/todo')


@login_required
@current_required
def todo_delete(request):
    todo_id = int(request.query.get('id', -1))
    if todo_id == -1:
        # 没找到, 返回错误页面
        return error(request)
    Todo.delete(todo_id)
    return redirect('/todo')


route_dict = {
    '/todo': todo_index,
    '/todo/add': todo_add,
    '/todo/edit': todo_edit,
    '/todo/update': todo_update,
    '/todo/delete': todo_delete,
}

