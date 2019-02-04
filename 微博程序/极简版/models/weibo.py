from models import Model
from models.user import User


class Weibo(Model):
    def __init__(self, form):
        super().__init__()
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', -1)

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
        self.weibo_id = form.get('weibo_id', -1)

    def user(self):
        """
        返回这篇评论的用户
        """
        u = User.find_by(id=self.user_id)
        return u

