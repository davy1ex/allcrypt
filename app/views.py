# Сделать:
# -- добавить символы (_*:^!@) для генерация пароля

import random
from datetime import datetime
import string # для халявного словаря латинских симолов
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message

from app import app, db, mail
from app.forms import RegistrationForm, LoginForm, AddForm, IndexForm, GenPassForm, ChangePasswordForm, ResetPasswordForm, SettingsEmailForm, SettingsKeyForm, SettingsForm
from app.models import User, Account

from aes import AESCrypt  # Модуль по шифрации с форума


def generate_pass(numbers, symbols, length, letters=True):
    """ генерация пароля заданной длины из запрашиваемых сиволов """
    symbols_line = "!@#$%^&*()/+_-?,."
    password = ""
    row = []
    if letters:
        row.append(string.ascii_letters)
    
    if numbers:
        row.append("0123456789")
    
    if symbols:
        row.append(symbols_line)
    
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
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            user.set_key(form.key.data)
            db.session.add(user)
            db.session.commit()
        
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
            flash("Oops... Your password/login incorrect.")            
            return redirect("/login")
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    return render_template("login.html", form=form)


# главная страница
@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    form = IndexForm()
    accounts = []
    account_types = ["Email", "Social", "Games", "Work", "Other"]
    decrypted_passwords = []  # список, который будет содержать упорядоченный по типу аккаунта пароли
    if form.validate_on_submit():
        
        if request.form["submit"] == "show/hide all":
            if form.key.data == "":
                return redirect(url_for("index"))
            
            else:
                if current_user.check_key(form.key.data):
                    # список дешифрованных паролей. AESCryptУ нужен ключ, дальше метод decrypt() возвращает дешифрованный пароль
                    # decrypted_passwords = [AESCrypt(form.key.data).decrypt(account.password) for account in accounts.all()]

                    # создание двух списков - аккаунтов и дешифрованных паролей, упорядоченных по порядку типов
                    for account_type in account_types:
                        decrypted_passwords.append({account_type: []})
                        
                        for account in Account.query.filter_by(master=current_user, account_type=account_type).all():
                            decrypted_passwords[account_types.index(account_type)][account_type].append(AESCrypt(form.key.data).decrypt(account.password))
                            accounts.append(account)
                    print(decrypted_passwords)
                    return render_template("index/index.html", title="home", form=form, accounts=Account, decrypted_passwords=decrypted_passwords, account_types=account_types)
        else:
            db.session.delete(Account.query.filter_by(id=request.form["submit"]).first())
            db.session.commit()
    return render_template("index/index.html", title="home", form=form, accounts=Account, account_types=account_types)


# добавляет новые записи
@app.route("/index/add", methods=["GET", "POST"])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        key = form.key.data
        
        if current_user.check_key(key):
            account = Account(login=form.login.data, password=AESCrypt(key).encrypt(form.password.data), master=current_user, account_type=request.form.get("account_type"))
            db.session.add(account)
            db.session.commit()
            flash("Writed.")
        
        else:
            flash("Key incorrect.")
            return redirect("/index/add")
        
        return redirect("/")
    return render_template("index/add.html", form=form)


@app.route("/index/generate", methods=["GET", "POST"])
def generate():
    form = GenPassForm()
    if form.validate_on_submit():
        numbers = False
        # letters = False
        symbols = False
        
        if request.form.get("letters"):
            letters = True
        
        if request.form.get("numbers"):
            numbers = True
        
        if request.form.get("symbols"):
            symbols = True
        
        elif not request.form.get("letter") and not request.form.get("numbers"):
            flash("You must select at least one checkbox.")
            return redirect("/index/generate")
        
        length = form.input_field.data
        flash(generate_pass(letters=letters, numbers=numbers, symbols=symbols, length=length))
    return render_template("index/generate.html", form=form)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        if request.form["submit"] == "clear all accounts":
            db.session.query(Account).filter_by(master=current_user).delete()
            db.session.commit()
            flash("All accounts deleted.")
            
            return redirect("/settings")
    return render_template("settings/settings.html", form=form)


# страница с настройками (Тёмная тема ис каминг)
@app.route("/change_password", methods=["GET", "POST"])
@app.route("/settings/password", methods=["POST", "GET"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.commit()
        flash("Success.")
        
        return redirect(url_for("settings"))
    return render_template("settings/password.html", form=form)


@app.route("/settings/email", methods=["GET", "POST"])
@login_required
def settings_email():
    form = SettingsEmailForm()
    if form.validate_on_submit():
        if request.form["submit"] == "send code":
            mail.send(Message(str(current_user.generate_validate_code()), sender="ludmila89272671892@gmail.com", recipients=[current_user.email]))
            db.session.commit()
            flash("Check your email. (code valid for 5 minutes)")
        
        elif request.form["submit"] == "validate":
            if datetime.now() <= current_user.time_to_validate and current_user.check_validate_code(form.code.data):
                current_user.validate()
                db.session.commit()
                flash("Your account was validated.")
            else:
                flash("Invalid/overdue code.")

        elif request.form["submit"] == "change":
            if form.email.data != "" and "@" in form.email.data and "." in form.email.data:
                current_user.change_email(form.email.data)
                current_user.devalidate()
                db.session.commit()
                flash("Successfully. Please confirm the new mail.")
            
            else:
                flash("You must input email.")
    return render_template("settings/email.html", form=form)


@app.route("/settings/key", methods=["GET", "POST"])
@login_required
def settings_key():
    form = SettingsKeyForm()
    if form.validate_on_submit():
        if request.form["submit"] == "change" and form.key.data != "":
            current_user.set_key(form.key.data)
            db.session.commit()
            flash("Successfully.")
    return render_template("settings/key.html", form=form)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if request.form["submit"] == "send code":
            user = User.query.filter_by(email=form.email.data).first()
            
            if user is not None:
                with app.app_context():
                    mail.send(Message(str(user.generate_validate_code()), sender="ludmila89272671892@gmail.com", recipients=[user.email]))
                    db.session.commit()
                    flash("Check your email.")
            
            else:
                flash("Invalid email.")

        elif request.form["submit"] == "submit":
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None:
                if user.check_validate_code(form.code.data) and datetime.now() <= user.time_to_validate:
                    login_user(user, remember=False)
                    return redirect("/change_password")
                
                elif datetime.now() > user.time_to_validate:
                    flash("Validation code overdue.")
                
                else:
                    flash("Invalid code.")
            else:
                flash("Invalid username.")
        return redirect("/reset_password")
    return render_template("reset_password/reset_password.html", form=form)


# страница "выйти"
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
