from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
lm = LoginManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)


def create_app():

    from .views import Register, Login, Dashboard, Logout, UsersAPI, ProductsAPI
    app.add_url_rule("/register", view_func=Register.as_view("register"))
    app.add_url_rule("/login", view_func=Login.as_view("login"))
    app.add_url_rule("/dashboard", view_func=Dashboard.as_view("dashboard"))
    app.add_url_rule("/logout", view_func=Logout.as_view("logout"))

    user_view = UsersAPI.as_view('user_api')
    app.add_url_rule('/users/', defaults={'user_id': None}, view_func=user_view, methods=['GET', ])
    app.add_url_rule('/users/', view_func=user_view, methods=['POST', ])
    app.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'DELETE'])

    return app
