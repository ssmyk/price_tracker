from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import Config

app = Flask(__name__)
db = SQLAlchemy()
lm = LoginManager()
bcrypt = Bcrypt(app)


def create_app():
    app.config.from_object(Config)
    db.init_app(app)
    lm.init_app(app)
    from .views import Register, Login, Dashboard, Logout

    app.add_url_rule("/register", view_func=Register.as_view("register"))
    app.add_url_rule("/login", view_func=Login.as_view("login"))
    app.add_url_rule("/dashboard", view_func=Dashboard.as_view("dashboard"))
    app.add_url_rule("/logout", view_func=Logout.as_view("logout"))

    return app
