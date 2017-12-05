from flask import request, redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.mongoengine import ModelView, filters
from flask_admin.babel import lazy_gettext
from flask_security import current_user, login_required, roles_required
from jinja2 import Markup


from aquizz import models


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
        # Questions
        self._template_args['all_questions_count'] = models.Question.objects().count()
        self._template_args['ready_questions_count'] = models.Question.objects(
            __raw__={'$where': 'this.options.length >= 4'}).count()
        self._template_args['incomplete_questions_count'] = models.Question.objects(
            __raw__={'$where': 'this.options.length < 4'}).count()
        # Quizzes
        self._template_args['total_quizzes_count'] = models.Quiz.objects.count()
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
        FilterArrayLengthHigherOrEqual(column=models.Question.options, name='Options'),
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
    column_type_formatters = {
        list: list_br_formatter
    }
    column_filters = (
        'started_at',
        'finished_at',
        'player_name',
    )
