from models import Model
from utils import hashed_password, salted_password


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

        # 这里需要将数据库里面的密文 和 摘要算法加密以后的密码进行比较
        u = self.find_by(username=self.username)
        return u is not None and u.password == salted_password(self.password)

    def validate_register(self):
        """
        验证用户注册并对得到的密码加密
        """
        self.password = salted_password(self.password)
        if User.find_by(username=self.username) is None:
            # 没找到数据, 说明可以注册
            User.add(self)
            return self
        else:
            return None

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
