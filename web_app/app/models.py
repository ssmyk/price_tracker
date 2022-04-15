from __future__ import annotations
from flask_login import UserMixin
from . import db, bcrypt, ma
from .forms import RegisterForm
from flask_marshmallow import fields


def add_to_db(db_entry: Users | Products) -> None:
    """
    Adds a new entry to database.
    """
    db.session.add(db_entry)
    db.session.commit()


def delete_from_db(db_entry: Users | Products) -> None:
    """
    Deletes specific entry from database.
    """
    db.session.delete(db_entry)
    db.session.commit()


class Users(db.Model, UserMixin):
    """
    Users database model. Stores all registered users.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    products = db.relationship("Products", backref="users", lazy=True)

    def __init__(self, username: str, email: str, password:str) -> None:
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def email_validator(email: str) -> bool:
        """
        Checks if provided email address is already registered in database.
        """

        return Users.query.filter_by(email=email).first() is not None

    @staticmethod
    def create_user(form: RegisterForm) -> Users:
        """
        Creates Users object from register form.
        """
        user = Users(
            username=form.username.data,
            email=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data).decode("utf-8"),
        )
        return user

    @staticmethod
    def create_from_json(json_body: dict) -> Users:
        """
        Creates Users object from JSON.
        """
        return Users(
            username=json_body["username"],
            email=json_body["email"],
            password=json_body["password"],
        )


class Products(db.Model):
    """
    Products database model. Stores all tracked products.
    """

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    product_image = db.Column(db.String)
    product_asin = db.Column(db.String)
    date_added = db.Column(db.DateTime)
    current_price = db.Column(db.Float)
    current_price_date = db.Column(db.DateTime)
    lowest_price = db.Column(db.Float)
    lowest_price_date = db.Column(db.DateTime)
    fk_user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(
        self,
        product_name,
        product_image,
        product_asin,
        date_added,
        current_price,
        current_price_date,
        lowest_price,
        lowest_price_date,
        fk_user,
    ):
        self.product_name = product_name
        self.product_image = product_image
        self.product_asin = product_asin
        self.date_added = date_added
        self.current_price = current_price
        self.current_price_date = current_price_date
        self.lowest_price = lowest_price
        self.lowest_price_date = lowest_price_date
        self.fk_user = fk_user

    @staticmethod
    def create_from_json(json_body: dict) -> Products:
        """
        Creates Products object from JSON.
        """
        return Products(
            product_name=json_body["product_name"],
            product_image=json_body["product_image"],
            product_asin=json_body["product_asin"],
            date_added=json_body["date_added"],
            current_price=json_body["current_price"],
            current_price_date=json_body["current_price_date"],
            lowest_price=json_body["lowest_price"],
            lowest_price_date=json_body["lowest_price_date"],
            fk_user=json_body["fk_user"],
        )


class UserSchema(ma.Schema):
    """
    Defines output format after serialization for Users object.
    """

    _id = fields.fields.Integer()
    username = fields.fields.Str()
    email = fields.fields.Str()
    password = fields.fields.Str()


class ProductSchema(ma.Schema):
    """
    Defines output format after serialization for Products object.
    """

    _id = fields.fields.Integer()
    product_name = fields.fields.Str()
    product_image = fields.fields.Str()
    product_asin = fields.fields.Str()
    date_added = fields.fields.DateTime()
    current_price = fields.fields.Float()
    current_price_date = fields.fields.DateTime()
    lowest_price = fields.fields.Float()
    lowest_price_date = fields.fields.DateTime()
    fk_user = fields.fields.Integer()
