from models import Model


class Message(Model):
    def __init__(self, data):
        super().__init__(data)
        self.author = data.get('author', '')
        self.message = data.get('message', '')
