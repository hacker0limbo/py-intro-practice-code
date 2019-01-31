from models import Model


class Todo(Model):
    def __init__(self, form):
        # form 值的是 数据库里面存取的数据, 读出以后格式为字典
        super().__init__()
        self.id = form.get('id', None)
        self.title = form.get('title', '')
        self.user_id = form.get('user_id', -1)

    @classmethod
    def update(cls, id, title):
        todos = cls.all()
        for t in todos:
            if t.id == id:
                t.title = title
        cls.save(todos)

    @classmethod
    def remove(cls, id):
        """
        删除一个 todo 的时候 其他的 todo 的 id
        """
        todos = cls.all()
        for t in todos:
            if t.id == id:
                todos.remove(t)
                break
        cls.save(todos)

    @classmethod
    def add(cls, todo, user_id):
        """
        增加一个 todo
        """
        todos = cls.all()
        # 新加的 id 需要重设 id
        todo.id = len(todos) + 1
        todo.user_id = user_id
        todos.append(todo)
        cls.save(todos)


