from __future__ import annotations
from flask_login import UserMixin
from . import db, app, bcrypt
import os
from .forms import RegisterForm

def create_db() -> None:
    if not os.path.exists('users.sqlite3'):
        with app.app_context():
            db.create_all()

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def add_to_db(user: Users) -> None:
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def email_validator(email: str) -> bool:
        if Users.query.filter_by(email=email).first():
            return True
        return False

    @staticmethod
    def create_user(form: RegisterForm) -> Users:
        user = Users(username = form.username.data, email=form.email.data, password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
        return user

