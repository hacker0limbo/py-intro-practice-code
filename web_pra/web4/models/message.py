from models import Model


class Message(Model):
    def __init__(self, form):
        super().__init__()
        self.author = form.get('author', '')
        self.message = form.get('message', '')
