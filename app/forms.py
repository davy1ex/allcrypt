from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email


class RegistrationForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired(), ])
    password2 = PasswordField("repeat password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign up")
    


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")

