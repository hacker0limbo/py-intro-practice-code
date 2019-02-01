from models import Model
from models.user import User


class Weibo(Model):
    def __init__(self, form, user_id=-1):
        super().__init__()
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        self.deleted = form.get('deleted', False)

    @classmethod
    def add(cls, weibo, user_id):
        """
        增加一个新的 weibo, 同时加上当前 user_id
        """
        weibos = cls.all()
        weibo.id = len(weibos) + 1
        weibo.user_id = int(user_id)
        weibos.append(weibo)
        cls.save(weibos)

    @classmethod
    def delete(cls, id):
        weibos = cls.all()
        for w in weibos:
            if w.id == id:
                w.deleted = True
        cls.save(weibos)

    @classmethod
    def update(cls, id, content):
        weibos = cls.all()
        for w in weibos:
            if w.id == id:
                w.content = content
        cls.save(weibos)

    def comments(self):
        """
        返回该篇博文里面的所有评论
        """
        return Comment.find_all(weibo_id=self.id)


class Comment(Model):
    def __init__(self, form, user_id=-1):
        super().__init__()
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = int(form.get('weibo_id', -1))

    def user(self):
        """
        返回这篇评论的用户
        """
        u = User.find_by(id=self.user_id)
        return u

    @classmethod
    def add(cls, comment):
        comments = cls.all()
        comment.id = len(comments) + 1
        comments.append(comment)
        cls.save(comments)
