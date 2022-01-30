from flask import Blueprint, request, render_template
from .forms import RegisterForm, LoginForm
from . import db
from .models import Users

main_blueprint = Blueprint('main',__name__)

@main_blueprint.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Users(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        #return 'elo'
    return render_template('register.html',form=form)

@main_blueprint.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():

        return 'elo'
    return render_template('login.html',form=form)





