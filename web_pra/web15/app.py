import os
from flask import Flask
from models import db
from models.user import User
from models.message import Message


from routes.index import index_bp as index_routes
from routes.message import message_bp as message_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'db', 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'limboer'
db.init_app(app)

app.register_blueprint(index_routes)
app.register_blueprint(message_routes, url_prefix='/message')


if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)