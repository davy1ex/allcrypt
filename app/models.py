from flask import SQLAlchemy
from app import db


class User(db.Model):
    id = db.Coulumn(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    login = db.Column(db.String(64), unique=True, index=True, default=email.split('@')[0])

    password_hash = db.Column(db.String(128))
    account.db.relationship('Account', backref='master')

    def __repr__(self):
        return '<User {}>'.format(self.login)
