# Сделать:
# -- добавить символы (_*:^!@) для генерация пароля

import random
import string # для халявного словаря латинских симолов
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.forms import RegistrationForm, LoginForm, AddForm, IndexForm, GenPass
from app.models import User, Account

from aes import AESCrypt # Модуль по шифрации с форума


def generate_pass(numbers, length, letters=True):
    """ генерация пароля заданной длины из запрашиваемых сиволов """
    password = ""
    row = []
    if letters:
        row.append(string.ascii_letters)
    if numbers:
        row.append("0123456789")
    for _ in range(int(length)):
        password += random.choice(random.choice(row))
    return password


# страница регистации
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
            user.set_key(form.key.data)
            db.session.add(user)
            db.session.commit()
        flash("Теперь ты наш")
        return redirect(url_for("login"))
    return render_template("reg.html", form=form)


# страница авторизации
@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Oops... You're password/login incorrect")
            return redirect("/login")
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    return render_template("login.html", form=form)


# главная страница
@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    form = IndexForm()
    accounts = Account.query.filter_by(master=current_user)
    if form.validate_on_submit():
        # else:
        #     return request.form["hide"]
        if request.form["submit"] == "show/hide all":
            if form.key.data == "":
                return redirect(url_for("index"))
            else:
                if current_user.check_key(form.key.data):
                    decrypted_passwords = [AESCrypt(form.key.data).decrypt(account.password) for account in accounts.all()]
                    return render_template("index.html", title="home", form=form, accounts=accounts, decrypted_passwords=decrypted_passwords)
        else:
            db.session.delete(Account.query.filter_by(id=request.form["submit"]).first())
            db.session.commit()
    return render_template("index.html", title="home", form=form, accounts=accounts)


# НЁХ
@app.route("/parser", methods=["GET", "POST"])
@login_required
def parser():
    pass
    # return redirect(url_for("index"))            


# добавляет новые записи
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        key = form.key.data
        if current_user.check_key(key):
            account = Account(login=form.login.data, password=AESCrypt(key).encrypt(form.password.data), master=current_user)
            db.session.add(account)
            db.session.commit()

            flash("Writed")
            return redirect(url_for("index"))
    return render_template("add.html", form=form)


# страница с настройками (Тёмная тема ис каминг)
@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")


@app.route("/generate", methods=["GET", "POST"])
def generate():
    form = GenPass()
    if form.validate_on_submit():
        text = ""
        numbers = False
        letters = False
        if request.form.get("letters"):
            letters = True
        if request.form.get("numbers"):
            numbers = True
        length = form.input_field.data
        flash(generate_pass(letters=letters, numbers=numbers, length=length))
    return render_template("generate.html", form=form)


# страница "выйти"
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
