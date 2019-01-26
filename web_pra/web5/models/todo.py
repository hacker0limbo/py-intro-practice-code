from models import Model


class Todo(Model):
    def __init__(self, form):
        super().__init__()
        # self.id = form.get('id', None)
        self.title = form.get('title', '')

    @classmethod
    def update(cls, id, title):
        todos = cls.all()
        for t in todos:
            if t.id == id:
                t.title = title
        cls.save(todos)

    @classmethod
    def remove(cls, id):
        todos = cls.all()
        for t in todos:
            if t.id == id:
                todos.remove(t)
                break
        cls.save(todos)


