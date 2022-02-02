from flask import request, render_template
from .forms import RegisterForm, LoginForm
from .models import Users
from . import lm, bcrypt
from flask_login import login_user
from flask.views import MethodView


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
                Users.add_to_db(user)
                return "You account has been created"
            return "Email is already registered"


class Login(MethodView):
    def __init__(self):
        self.template_name = 'login.html'
    def get(self):
        form = LoginForm()
        return render_template(self.template_name, form=form)

    def post(self):
        form = LoginForm(request.form)
        if Users.email_validator(form.email.data):
            user = Users.query.filter_by(email=form.email.data).first()
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return "You are logged"
        return "Incorrect data"
