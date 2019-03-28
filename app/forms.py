from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat password", validators=[DataRequired(), EqualTo("password")])
    key = PasswordField("Key", validators=[DataRequired()])
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
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("sign in")


class GenPassForm(FlaskForm):
    input_field = StringField("Length", validators=[DataRequired()])


class AddForm(FlaskForm):
    login = StringField("login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    key = PasswordField("Please, enter your key", validators=[DataRequired()])
    submit = SubmitField("add")


class IndexForm(FlaskForm):
    key = PasswordField("Key")
    submit = SubmitField("show/hide all")
    submit = SubmitField("delete")


class SettingsForm(FlaskForm):
    submit = SubmitField("")


class ChangePasswordForm(FlaskForm):
    password = PasswordField("Your new password", validators=[DataRequired()])
    password2 = PasswordField("Repeat password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("reset")


class ResetPasswordForm(FlaskForm):
    username = StringField("Username")
    email = StringField("Email")
    code = StringField("Your code")
    submit = SubmitField()


class SettingsEmailForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    code = StringField("Code")
    submit = SubmitField("Submit")


class SettingsKeyForm(FlaskForm):
    key = PasswordField("New key")
    submit = SubmitField("Submit")
