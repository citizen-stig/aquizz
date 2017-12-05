import importlib
import os

from flask import Flask, send_file
from flask_admin import Admin
from flask_restful import Api
from flask_security import Security


from aquizz.models import db
from aquizz.admin import AdminProtectedModelView, AdminProtectedIndexView, QuestionAdminView, QuizAdminView
from aquizz.models import Question, User, Quiz, user_datastore
from aquizz.api import QuizListResource, QuizResource


def create_app():

    settings = os.getenv('FLASK_SETTINGS', 'develop')
    try:
        config_module = importlib.import_module('aquizz.settings.' + settings)
        config_obj = config_module.Config
    except (ImportError, AttributeError):
        config_module = importlib.import_module('aquizz.settings.' + 'develop')
        config_obj = config_module.Config
    app = Flask(__name__, static_folder=config_obj.STATIC_FOLDER)
    app.config.from_object(config_obj)
    db.init_app(app)

    @app.route('/')
    def home():
        return send_file(os.path.join(app.config['CLIENT_BUILD_FOLDER'], 'index.html'))

    @app.route('/favicon')
    def favicon():
        return send_file(os.path.join(app.config['CLIENT_BUILD_FOLDER'], 'favicon.ico'))

    if app.config['DEBUG']:
        @app.after_request
        def allow_standalone_client(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
            return response

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
                         index_view=AdminProtectedIndexView(),
                         template_mode='bootstrap3',
                         url='/admin')
    admin_portal.add_view(QuestionAdminView(Question))
    admin_portal.add_view(QuizAdminView(Quiz))
    return admin_portal


def setup_api(app):
    api = Api(app, prefix='/api/v1')
    # Auth
    api.add_resource(QuizListResource, '/quiz', endpoint='quiz')
    api.add_resource(QuizResource, '/quiz/<string:quiz_id>', endpoint='quiz_object')

