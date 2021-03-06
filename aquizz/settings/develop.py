import os
from .base import Config as BaseConfig


class Config(BaseConfig):
    DEBUG = True
    SECRET_KEY = 'super-secret'
    SECURITY_PASSWORD_SALT = os.getenv('FLASK_PASSWORD_SALT', 'some_salt')
