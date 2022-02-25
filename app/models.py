from __future__ import annotations
from flask_login import UserMixin
from . import db, app, bcrypt
import os
from .forms import RegisterForm
from .config import DBConfig


def create_db() -> None:
    if not os.path.exists(DBConfig.DB_NAME):
        with app.app_context():
            db.create_all()


def add_to_db(db_entry: Users | Products) -> None:
    db.session.add(db_entry)
    db.session.commit()


class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    #products = db.relationship('products', backref='products', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def email_validator(email: str) -> bool:
        if Users.query.filter_by(email=email).first():
            return True
        return False


    @staticmethod
    def create_user(form: RegisterForm) -> Users:
        user = Users(username=form.username.data,
                     email=form.email.data,
                     password=bcrypt.generate_password_hash(form.password.data).decode("utf-8"), )
        return user


class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    product_asin = db.Column(db.String, unique=True)
    date_added = db.Column(db.DateTime)
    current_price = db.Column(db.String)
    lowest_price = db.Column(db.String)
    #fk_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, product_name, product_asin, date_added, current_price, lowest_price):
        self.product_name = product_name
        self.product_asin = product_asin
        self.date_added = date_added
        self.current_price = current_price
        self.lowest_price = lowest_price


