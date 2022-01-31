from flask import Blueprint, request, render_template
from .forms import RegisterForm, LoginForm
from .models import Users
from . import lm, bcrypt
from flask_login import login_user

@lm.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

main_blueprint = Blueprint('main',__name__)

@main_blueprint.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        if not Users.email_validator(form.email.data):
            user = Users(username=form.username.data, email=form.email.data, password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
            Users.add_to_db(user)
            return 'You account has been created'
        return 'Email is already registered'
    return render_template('register.html',form=form)

@main_blueprint.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        if Users.email_validator(form.email.data):
            user = Users.query.filter_by(email=form.email.data).first()
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user)
                return 'You are logged'
    return render_template('login.html',form=form)





