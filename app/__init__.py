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
    from .views import main_blueprint
    app.register_blueprint(main_blueprint)
    return app