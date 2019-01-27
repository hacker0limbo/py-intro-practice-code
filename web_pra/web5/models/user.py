from models import Model


class User(Model):
    def __init__(self, form):
        super().__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')

    def validate_login(self):
        # users = self.all()
        # for user in users:
        #     if self.username == user.username and self.password == user.password:
        #         return True
        # return False
        u = self.find_by(username=self.username)
        return u is not None and u.password == self.password

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2 and (self.find_by(username=self.username) is None)

    @classmethod
    def add(cls, user):
        """
        增加一个 user
        """
        users = cls.all()
        # 新加的 id 需要重设 id
        user.id = len(users) + 1
        users.append(user)
        cls.save(users)


