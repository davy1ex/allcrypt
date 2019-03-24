from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    password2 = PasswordField("repeat password", validators=[DataRequired(), EqualTo("password")])
    key = PasswordField("key", validators=[DataRequired()])
    submit = SubmitField("register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("user with this nickname already exist")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("user with this email already exist")


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember me")
    submit = SubmitField("sign in")


class GenPass(FlaskForm):
    input_field = StringField("length", validators=[DataRequired()])


class AddForm(FlaskForm):
    login = StringField("login", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    key = PasswordField("please, enter your key", validators=[DataRequired()])
    submit = SubmitField("add")


class IndexForm(FlaskForm):
    key = PasswordField("key")
    submit = SubmitField("show/hide all")
    submit = SubmitField("delete")


class SettingsForm(FlaskForm):
    submit = SubmitField("reset password")
    code_field = StringField("Code")
    submit = SubmitField("Ok")


class ResetPassword(FlaskForm):
    username = StringField("current username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    password2 = PasswordField("repeat password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("reset")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError("username is not found")
