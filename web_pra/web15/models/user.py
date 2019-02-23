from models import db
from utils import sha256


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

    def __init__(self, form: dict):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def salted_password(self, password, salt='abcdefg'):
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    @classmethod
    def add(cls, user):
        db.session.add(user)
        db.session.commit()

    @classmethod
    def find_by(cls, **kwargs):
            return cls.query.filter_by(**kwargs).first()

    @classmethod
    def register(cls, form: dict):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and cls.find_by(username=name) is None:
            print('未注册过')
            # 说明未注册过
            u = cls(form)
            u.password = u.salted_password(pwd)
            cls.add(u)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form: dict):
        u = cls(form)
        # 这里注意查询的时候需要使用 .first() 可以保证当没有查询到的时候可以返回 None
        user = cls.find_by(username=u.username)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        return None
