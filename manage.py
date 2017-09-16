from flask_script import Manager, Command, Option

from aquizz import app as app_factory
from aquizz import models
from aquizz import utils


class CreateAdminUser(Command):

    option_list = (
        Option('--email', '-e', dest='email'),
        Option('--password', '-p', dest='password'),
    )

    def run(self, email, password):
        admin_role = models.user_datastore.find_or_create_role('admin')
        # admin_user = models.User(email=email)
        admin_user = models.user_datastore.create_user(email=email, password=password)
        models.user_datastore.add_role_to_user(admin_user, admin_role)


class LoadBaseQuestions(Command):

    option_list = (
        Option('--filename', '-f', dest='filename'),
    )

    def run(self, filename):
        utils.load_data_from_file(filename)


if __name__ == '__main__':
    app = app_factory.create_app()
    manager = Manager(app)
    manager.add_command('create_admin_user', CreateAdminUser())
    manager.add_command('load_base', LoadBaseQuestions())
    manager.run()
