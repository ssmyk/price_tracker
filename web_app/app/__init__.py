from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import Config
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
lm = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
ma = Marshmallow()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    from .views import (
        Register,
        Login,
        Dashboard,
        Logout,
        UsersAPI,
        ProductsAPI,
        ProductUpdateAPI,
    )

    app.add_url_rule("/register", view_func=Register.as_view("register"))
    app.add_url_rule("/login", view_func=Login.as_view("login"))
    app.add_url_rule("/", view_func=Login.as_view(""))
    app.add_url_rule("/dashboard", view_func=Dashboard.as_view("dashboard"))
    app.add_url_rule("/logout", view_func=Logout.as_view("logout"))

    user_view = UsersAPI.as_view("user_api")
    app.add_url_rule(
        "/users/", defaults={"user_id": None}, view_func=user_view, methods=["GET"]
    )
    app.add_url_rule("/users/", view_func=user_view, methods=["POST"])
    app.add_url_rule(
        "/users/<int:user_id>", view_func=user_view, methods=["GET", "DELETE"]
    )

    product_view = ProductsAPI.as_view("product_api")
    app.add_url_rule(
        "/products/",
        defaults={"product_id": None},
        view_func=product_view,
        methods=["GET"],
    )
    app.add_url_rule("/products/", view_func=product_view, methods=["POST"])
    app.add_url_rule(
        "/products/<int:product_id>", view_func=product_view, methods=["GET", "DELETE"]
    )

    product_update_view = ProductUpdateAPI.as_view("product_update_api")
    app.add_url_rule(
        "/products/update/", view_func=product_update_view, methods=["POST"]
    )

    db.init_app(app)
    lm.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    return app
