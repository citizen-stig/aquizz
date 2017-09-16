import importlib
import os

from flask import Flask
from flask_admin import Admin
from flask_restful import Api
from flask_security import Security


from aquizz.models import db
from aquizz.admin import AdminProtectedModelView, QuestionAdminView
from aquizz.models import Question, User, user_datastore
from aquizz.api import QuizListResource, QuizResource


def create_app():
    app = Flask(__name__)
    settings = os.getenv('FLASK_SETTINGS', 'develop')
    try:
        config_module = importlib.import_module('aquizz.settings.' + settings)
        config_obj = config_module.Config
    except (ImportError, AttributeError):
        config_module = importlib.import_module('aquizz.settings.' + 'develop')
        config_obj = config_module.Config

    app.config.from_object(config_obj)
    db.init_app(app)
    # FIXME: Workaround for flask-mongoengine 0.8 issue
    # https://github.com/MongoEngine/flask-mongoengine/issues/259
    # mongodb_settings = app.config['MONGODB_SETTINGS']
    # if mongodb_settings.get('username') and mongodb_settings.get('password'):
    #     app.before_first_request(
    #         lambda: db.connection.authenticate(mongodb_settings.get('username'),
    #                                            mongodb_settings.get('password')))

    @app.route('/')
    def home():
        return 'Hello World!'

    Security(app, user_datastore)
    setup_admin(app)
    setup_api(app)
    return app


def setup_admin(app):
    """
    :param app:
    :return:
    """
    admin_portal = Admin(app,
                         name='aquizz',
                         template_mode='bootstrap3',
                         url='/admin')
    admin_portal.add_view(QuestionAdminView(Question))
    return admin_portal


def setup_api(app):
    api = Api(app, prefix='/api/v1')
    # Auth
    api.add_resource(QuizListResource, '/quiz', endpoint='quiz')
    api.add_resource(QuizResource, '/quiz/<string:quiz_id>', endpoint='quiz_object')

