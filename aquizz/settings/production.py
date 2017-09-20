import os
from .base import Config as BaseConfig


class Config(BaseConfig):
    DEBUG = False
    Testing = False
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']
    SECURITY_PASSWORD_SALT = os.environ['FLASK_PASSWORD_SALT']
    MONGODB_SETTINGS = os.environ['MONGOENGINE_URI']

