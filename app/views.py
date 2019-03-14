import random
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.forms import RegistrationForm, LoginForm, AddForm, IndexForm
from app.models import User, Account


@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    form = IndexForm()
    accounts = Account.query.all()
    return render_template("index.html", title="home", form=form, accounts=accounts)


@app.route("/delete_by_id")
@login_required
def delete_by_id():
    form = IndexForm()
    db.session.delete(Account.query.filter_by(id=request.args.get("submit")).first())
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        account = Account(login=form.login.data, password=form.login.data, master=user)
        db.session.add(account)
        db.session.commit()

        flash("Writed")
        return redirect(url_for("index"))
    return render_template("add.html", form=form)


@app.route("/reg", methods=["POST", "GET"])
def reg():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, email=form.email.data).first()
        if user is None:
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
        flash("Теперь ты наш")
        return redirect(url_for("login"))
    return render_template("reg.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Упс, кажется, что-то ввелось неверно...")
            return redirect("/login")
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/generate")
@login_required
def generate():
    return str(random.random())
