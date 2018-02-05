import statistics
from flask_script import Manager, Command, Option
import numpy as np

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


class PrintStat(Command):

    def run(self):
        completed_quizzes = models.Quiz.objects()
        scores = []
        for quiz in completed_quizzes:
            if quiz.finished_at:
                scores.append(quiz.get_score())
        # print(scores)
        print('Avg: ', statistics.mean(scores))
        print('Median:', statistics.median(scores))
        a = np.array(scores)
        print('p90:', np.percentile(a, 90))


if __name__ == '__main__':
    app = app_factory.create_app()
    manager = Manager(app)
    manager.add_command('create_admin_user', CreateAdminUser())
    manager.add_command('load_base', LoadBaseQuestions())
    manager.add_command('print_stat', PrintStat())
    manager.run()
