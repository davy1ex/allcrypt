# Сделать:
#   -- реализовать миграции

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    key_hash = db.Column(db.String(64))
    account = db.relationship("Account", backref="master", lazy="dynamic")

    def __repr__(self):
        return "<User \"{}\">".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_key(self, key):
        self.key_hash = generate_password_hash(key)

    def check_key(self, key):
        return check_password_hash(self.key_hash, key)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))       
    login = db.Column(db.String(64), index=True)
    # password_hash = db.Column(db.String(120), index=True)
    password = db.Column(db.String(120), index=True)

    def __repr__(self):
        return "<Account #{0}>".format(self.id)
