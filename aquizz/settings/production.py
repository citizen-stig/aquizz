import os
from .base import Config as BaseConfig
from pymongo.uri_parser import parse_uri


def get_mongodb_settings():
    connection_string = os.environ['MONGODB_URI']
    parsed = parse_uri(connection_string)
    first_node = parsed['nodelist'][0]
    host, port = first_node
    return {
        'host': host,
        'port': port,
        'db': parsed['database'],
        'username': parsed['username'],
        'password': parsed['password']}


class Config(BaseConfig):
    DEBUG = False
    Testing = False
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']
    SECURITY_PASSWORD_SALT = os.environ['FLASK_PASSWORD_SALT']
    MONGODB_SETTINGS = get_mongodb_settings()

