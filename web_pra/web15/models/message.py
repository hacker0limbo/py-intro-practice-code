from models import db, Model
import time
from utils import current_time


class Message(Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    author = db.Column(db.String)
    created_time = db.Column(db.Integer)
    deleted = db.Column(db.Boolean)

    def __init__(self, form: dict):
        self.content = form.get('content', '')
        self.author = form.get('author', '')
        self.created_time = int(time.time())
        self.deleted = False

    @classmethod
    def delete(cls, id):
        m = cls.query.get(id)
        m.deleted = True
        db.session.commit()
        return m

    @classmethod
    def update(cls, id, content):
        m = cls.query.get(id)
        m.content = content
        db.session.commit()
        return m

    def current_time(self):
        return current_time(self.created_time)