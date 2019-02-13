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
    body = j_template('todo_index.html')
    return http_response(body)


route_dict = {
    '/todo': todo_index,
}

