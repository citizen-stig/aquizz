import os


class Config(object):
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    CLIENT_BUILD_FOLDER = os.path.join(PROJECT_ROOT, 'aquizz-client', 'build')
    STATIC_FOLDER = os.path.join(CLIENT_BUILD_FOLDER, 'static')
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {
        'db': 'aquizz',
        'host': 'localhost',
        'port': 27017,
    }
