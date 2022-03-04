from flask import request, render_template, redirect, url_for
from .forms import RegisterForm, LoginForm
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
    return Users.query.get(int(user_id))

class Register(MethodView):
    def __init__(self):
        self.template_name = 'register.html'

    def get(self):
        form = RegisterForm()
        return render_template(self.template_name, form=form)

    def post(self):
        form = RegisterForm(request.form)
        if form.validate():
            if not Users.email_validator(form.email.data):
                user = Users.create_user(form)
                add_to_db(user)
                return "You account has been created"
            return "Email is already registered"
        return render_template(self.template_name, form=form)


class Login(MethodView):
    def __init__(self):
        self.template_name = 'login.html'

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        form = LoginForm()
        return render_template(self.template_name, form=form)

    def post(self):
        form = LoginForm(request.form)
        if Users.email_validator(form.email.data):
            user = Users.query.filter_by(email=form.email.data).first()
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
        return "Incorrect data"

class Dashboard(MethodView):
    def __init__(self):
        self.template_name = 'dashboard.html'

    @login_required
    def get(self):
        products = Products.query.all()
        return render_template(self.template_name, products=products)


class Logout(MethodView):
    def get(self):
        logout_user()
        return redirect(url_for('login'))


class UsersAPI(MethodView):
    @login_required
    def get(self, user_id):
        if user_id is None:
            all_users = Users.query.all()
            return users_schema.jsonify(all_users)
        found_user = Users.query.get(user_id)
        return user_schema.jsonify(found_user)

    def post(self):
        body = request.json
        new_user = Users.create_from_json(json_body=body)
        add_to_db(new_user)
        return user_schema.jsonify(new_user)

    def delete(self, user_id):
        user_to_delete = Users.query.get(user_id)
        delete_from_db(user_to_delete)
        return user_schema.jsonify(user_to_delete)

class ProductsAPI(MethodView):
    def get(self, product_id):
        if product_id is None:
            try:
                all_products = Products.query.all()
                return products_schema.jsonify(all_products), 200
            except:
                return 'Internal error', 500
        try:
            found_product = Products.query.get(product_id)
            return product_schema.jsonify(found_product), 200
        except:
            return 'Internal error', 500

    def post(self):
        try:
            body = request.json
            new_product = Products.create_from_json(json_body=body)
            add_to_db(new_product)
            return user_schema.jsonify(new_product), 200
        except:
            return 'Internal error', 500


    def delete(self, product_id):
        try:
            product_to_delete = Products.query.get(product_id)
            delete_from_db(product_to_delete)
            return user_schema.jsonify(product_to_delete), 200
        except:
            return 'Internal error', 500


