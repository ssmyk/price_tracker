from . import db

class Users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String())

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password