from flask import request, render_template, redirect, url_for, flash
from .forms import LoginForm
from .models import *
from . import lm, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flask.views import MethodView

user_schema = UserSchema()
users_schema = UserSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@lm.user_loader
def load_user(user_id):
    """
    Reloads the user from the user_id stored in session.
    """
    return Users.query.get(int(user_id))


class Register(MethodView):
    """
    Allows to register a new user.
    """

    def __init__(self):
        self.template_name = "register.html"

    def get(self) -> str:
        """
        Renders register site with register forms
        """
        form = RegisterForm()
        return render_template(self.template_name, form=form)

    def post(self) -> "Response" | str :
        """
        Allows to get request from register site to create a new user. Checks if a posted user is already in registered.
        """
        form = RegisterForm(request.form)
        if form.validate():
            if not Users.email_validator(form.email.data):
                user = Users.create_user(form)
                add_to_db(user)
                flash("You account has been created")
                return redirect(url_for("login"))
            flash("Email is already registered")
            return redirect(url_for("register"))
        return render_template(self.template_name, form=form)


class Login(MethodView):
    """
    View which allows users to log into to application.
    """

    def __init__(self):
        self.template_name = "login.html"

    def get(self):
        """
        Renders login site and login form. If the user is already logged redirects to dashboard site.
        """
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        form = LoginForm()
        return render_template(self.template_name, form=form)

    def post(self):
        """
        Allows to obtain login data provided by the user. Checks whether the user provided correct data and whether is registered in the system.
        """
        form = LoginForm(request.form)
        if not Users.email_validator(form.email.data):
            flash("User not registered")
            return redirect(url_for("login"))

        user = Users.query.filter_by(email=form.email.data).first()
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Invalid password provided")
        return redirect(url_for("login"))


class Dashboard(MethodView):
    """
    Main page of the application
    """

    def __init__(self):
        self.template_name = "dashboard.html"

    @login_required
    def get(self):
        """
        Displays information about tracked products of the logged in user.
        """
        products = Products.query.filter(Products.fk_user == current_user.id).order_by(
            Products.date_added
        )
        return render_template(self.template_name, products=products)


class Logout(MethodView):
    """
    Allows the user to log out.
    """

    def get(self):
        """
        Redirects logged out user to login site.
        """
        logout_user()
        flash("You have been logged out")
        return redirect(url_for("login"))


class UsersAPI(MethodView):
    """
    API to manage users.
    """

    @login_required
    def get(self, user_id: int):
        """
        Allows to obtain all users or a specific one.
        """
        if user_id is None:
            all_users = Users.query.all()
            return users_schema.jsonify(all_users), 200
        found_user = Users.query.get(user_id)
        return user_schema.jsonify(found_user), 200

    def post(self):
        """
        Creates user from JSON.
        """
        body = request.json
        new_user = Users.create_from_json(json_body=body)
        try:
            add_to_db(new_user)
            return "User created", 201
        except:
            return "Internal error", 500

    def delete(self, user_id: int):
        """
        Deletes user with specific ID.
        """
        user_to_delete = Users.query.get(user_id)
        try:
            delete_from_db(user_to_delete)
            return "User deleted", 200
        except:
            return "Internal error", 500


class ProductsAPI(MethodView):
    """
    API to manage products.
    """

    def get(self, product_id: int):
        """
        Allows to obtain all products or a specific one.
        """
        if product_id is None:
            all_products = Products.query.all()
            return products_schema.jsonify(all_products), 200
        found_product = Products.query.get(product_id)
        return product_schema.jsonify(found_product), 200

    def post(self):
        """
        Used by scraper to create a new product. Already existing product will not be replaced.
        """
        body = request.json
        found_product = Products.query.filter_by(
            fk_user=body["fk_user"], product_asin=body["product_asin"]
        ).first()
        if found_product:
            return "Conflict", 409
        new_product = Products.create_from_json(json_body=body)
        try:
            add_to_db(new_product)
            return "Product added to track", 201
        except:
            return "Internal error", 500

    def delete(self, product_id: int):
        """
        Allows to delete a product entry using a button on the dashboard.
        """
        product_to_delete = Products.query.get(product_id)
        try:
            delete_from_db(product_to_delete)
            return "Product deleted", 200
        except:
            return "Internal error", 500


class ProductUpdateAPI(MethodView):
    """
    API to let update product entry by scraper.
    """

    def post(self):
        """
        Updates product details depending on conditions.
        """
        body = request.json
        found_product = Products.query.filter_by(
            fk_user=body["fk_user"], product_asin=body["product_asin"]
        ).first()
        if body["price"] < found_product.lowest_price:
            found_product.lowest_price = body["price"]
            found_product.lowest_price_date = body["date"]
            found_product.current_price = body["price"]
            found_product.current_price_date = body["date"]
            db.session.commit()
            return "Product updated", 200
        else:
            found_product.current_price = body["price"]
            found_product.current_price_date = body["date"]
            db.session.commit()
            return "Product updated", 200
