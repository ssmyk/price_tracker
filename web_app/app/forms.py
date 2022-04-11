from wtforms import Form, StringField, PasswordField, validators, SubmitField


class RegisterForm(Form):
    username = StringField(
        "Username", [validators.DataRequired(), validators.Length(min=4, max=12)]
    )
    email = StringField(
        "Email address",
        [validators.DataRequired(), validators.Email(granular_message=True)],
    )
    password = PasswordField(
        "Create password", [validators.DataRequired(), validators.Length(min=3)]
    )
    confirm = PasswordField(
        "Repeat password",
        [
            validators.DataRequired(),
            validators.EqualTo("password", message="Passwords doesn't match"),
        ],
    )
    submit = SubmitField("Register")


class LoginForm(Form):
    email = StringField("Email", [validators.DataRequired()])
    password = PasswordField("Password")
    submit = SubmitField("Login")