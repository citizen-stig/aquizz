import pprint
from collections import defaultdict, OrderedDict

from flask import request, redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.babel import lazy_gettext
from flask_admin.contrib.mongoengine import ModelView, filters
from flask_security import current_user, login_required, roles_required
from jinja2 import Markup

from aquizz import models

pp = pprint.PrettyPrinter(indent=4)


class FilterArrayBaseLength(filters.BaseMongoEngineFilter):
    operator = '!='

    def apply(self, query, value):
        where = 'this.{field}.length {operator} {value}'.format(
            field=self.column.name,
            operator=self.operator,
            value=value
        )
        return query.filter(__raw__={'$where': where})

    def operation(self):
        return lazy_gettext('array_size {}'.format(self.operator))


class FilterArrayLengthLower(FilterArrayBaseLength):
    operator = '<'


class FilterArrayLengthHigherOrEqual(FilterArrayBaseLength):
    operator = '>='


class AdminProtectedIndexView(AdminIndexView):

    @expose()
    @login_required
    @roles_required('admin')
    def index(self):
        correct_answers = defaultdict(int)
        incorrect_answers = {}
        completed_quizzes = models.Quiz.objects(finished_at__ne='')
        all_questions = {}
        for quiz in completed_quizzes:
            for item in quiz.items:
                question_text = item.question.text
                if question_text not in all_questions:
                    all_questions[
                        question_text] = item.question.get_correct_options()
                if item.is_correct():
                    correct_answers[question_text] += 1
                else:
                    if question_text not in incorrect_answers:
                        incorrect_answers[question_text] = {
                            x.value: 0 for x in item.question.options
                        }
                    if item.answer not in incorrect_answers[question_text]:
                        # print('Error: {0}'.format(item))
                        continue
                    incorrect_answers[question_text][item.answer] += 1
        data = {}
        for question, correct_options in all_questions.items():
            incorrect = incorrect_answers.get(question)
            if incorrect is None:
                incorrect_count = 0
                incorrect_options = None
            else:
                incorrect_count = sum(incorrect.values())
                incorrect_options = OrderedDict(
                    sorted(((q, o) for q, o in incorrect.items() if o > 0),
                           key=lambda x: x[1],
                           reverse=True))
            incorrect_ratio = 0
            correct_count = correct_answers.get(question, 0)
            correct_ratio = 0
            total = incorrect_count + correct_count
            if correct_count > 0:
                correct_ratio = float(correct_count) / float(total)
            if incorrect_count > 0:
                incorrect_ratio = float(incorrect_count) / float(total)
            data[question] = {
                'total': total,
                'correct_count': correct_count,
                'correct_ratio': "{0:.0f}%".format(correct_ratio * 100.0),
                'correct_options': correct_options,
                'incorrect_count': incorrect_count,
                'incorrect_ratio': "{0:.0f}%".format(incorrect_ratio * 100.0),
                'incorrect_options': incorrect_options,
            }
        questions_analysis = list(
            sorted(
                data.items(),
                key=lambda x: x[1].get('incorrect_count'),
                reverse=True
            ))
        hardest_questions = questions_analysis[:20]
        simplest_questions = list(
            sorted(
                questions_analysis,
                key=lambda x: x[1].get('correct_count'),
                reverse=True)
        )[:10]
        self._template_args['hardest_questions'] = hardest_questions
        self._template_args['simplest_questions'] = simplest_questions
        # Questions
        self._template_args[
            'all_questions_count'] = models.Question.objects().count()
        self._template_args['ready_questions_count'] = models.Question.objects(
            __raw__={'$where': 'this.options.length >= 4'}).count()
        self._template_args[
            'incomplete_questions_count'] = models.Question.objects(
            __raw__={'$where': 'this.options.length < 4'}).count()
        # Quizzes
        self._template_args[
            'total_quizzes_count'] = models.Quiz.objects.count()
        self._template_args['completed_quizzes_count'] = models.Quiz.objects(
            finished_at__ne='').count()
        return super().index()


class AdminProtectedModelView(ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('admin'):
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class QuestionAdminView(AdminProtectedModelView):
    column_list = ('text', 'options')
    column_filters = (
        'text',
        FilterArrayLengthLower(column=models.Question.options, name='Options'),
        FilterArrayLengthHigherOrEqual(column=models.Question.options,
                                       name='Options'),
    )
    form_subdocuments = {
        'options': {
            'form_subdocuments': {
                None: {
                    'form_columns': ('value', 'is_correct')
                }
            }
        }
    }


def list_br_formatter(view, values):
    return Markup('<br/>'.join((str(x) for x in values)))


class QuizAdminView(AdminProtectedModelView):
    can_create = False
    can_edit = False
    can_delete = True
    can_view_details = True
    column_details_list = (
        'started_at',
        'finished_at',
        'player_name',
        'items'
    )
    column_default_sort = ('started_at', True)
    column_type_formatters = {
        list: list_br_formatter
    }
    column_filters = (
        'started_at',
        'finished_at',
        'player_name',
    )
