from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
