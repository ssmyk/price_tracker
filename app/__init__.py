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

    from .views import Register, Login, Dashboard, Logout
    app.add_url_rule("/register", view_func=Register.as_view("register"))
    app.add_url_rule("/login", view_func=Login.as_view("login"))
    app.add_url_rule("/dashboard", view_func=Dashboard.as_view("dashboard"))
    app.add_url_rule("/logout", view_func=Logout.as_view("logout"))

    return app
