from models import Model


class Message(Model):
    def __init__(self, form):
        super().__init__()
        self.author = form.get('author', '')
        self.message = form.get('message', '')

    @classmethod
    def add(cls, msg):
        """
        增加一个 user
        """
        msgs = cls.all()
        # 新加的 id 需要重设 id
        msg.id = len(msgs) + 1
        msgs.append(msg)
        cls.save(msgs)
