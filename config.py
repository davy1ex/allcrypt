import os


class Configuration(object):
    DEBUG = True
    SECRET_KEY = "RANDOM_KEY" # нужно будет придумать что получше
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.getcwd(), "app", "main.db")

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'ludmila89272671892'
    MAIL_PASSWORD = 'guburo42'