from models.todo import Todo
from routes import json_response
from routes.routes import current_user_id, login_required


def all(request):
    """
    返回当前用户的的所有 todo
    """
    u_id = current_user_id(request)
    todo_list = Todo.find_all(user_id=u_id)
    todos = [t.json_parse() for t in todo_list]
    return json_response(todos)


def add(request):
    """
    接受客户端发送的 json 数据, 添加数据并
    将新创建的 todo 数据返回给前端
    """
    # 得到 body 里面的数据
    user_id = current_user_id(request)
    form = request.json_parse()
    t = Todo(form)
    # 设置 user_id
    t.user_id = user_id
    Todo.add(t)
    # 返回新添加的数据
    return json_response(t.json_parse())


def delete(request):
    """
    前端根据 id 发送 ajax 到一个链接, 可以删除一个 todo
    比如发送到 /delete?id=1
    返回删除的 todo 数据
    """
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    Todo.delete(todo_id)
    return json_response(t.json_parse())


def update(request):
    """
    更新一个 todo, 发送过来的数据包含 id 和 title
    """
    form = request.json_parse()
    todo_title = form.get('title', '')
    todo_id = int(form.get('id', -1))
    Todo.update(todo_id, title=todo_title)
    t = Todo.find_by(id=todo_id)
    return json_response(t.json_parse())


route_dict = {
    '/api/todo/all': all,
    '/api/todo/add': add,
    '/api/todo/delete': delete,
    '/api/todo/update': update,
}