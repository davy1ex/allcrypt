from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required

from app import app
from app.models import User
from app.forms import RegistrationForm, LoginForm


@app.route("/")
def index():
    return render_template("index.html", title="home")


@app.route("/reg", methods=["POST", "GET"])
def reg():
    form = RegistrationForm()
    return render_template("reg.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("ты поц. Регистрируйся.")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    return render_template("login.html", form=form)


@app.route("/secret")
@login_required
def secret():
    return "fsdg"
