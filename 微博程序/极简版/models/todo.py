from models import Model


class Todo(Model):
    def __init__(self, form):
        # form 值的是 数据库里面存取的数据, 读出以后格式为字典
        self.id = form.get('id', None)
        self.title = form.get('title', '')
        self.user_id = form.get('user_id', -1)





