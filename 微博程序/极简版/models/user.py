from models import Model, open_db, close_db
from utils import salted_password


class User(Model):
    def __init__(self, form):
        # 初始化的时候不能有 id, 由于在 数据库里面 id 是自动增加的
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')

    def validate_login(self):
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
            conn, cursor = open_db()
            User.add(cursor, self)
            close_db(conn, cursor)
            return self
        else:
            return None
