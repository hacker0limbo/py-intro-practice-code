from models import Model

class User(Model):
    def __init__(self, data):
        super().__init__(data)
        self.username = data.get('username', '')
        self.password = data.get('password', '')

    def validate_login(self):
        users = self.all()
        for user in users:
            return self.username == user.username and self.password == user.password

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2
