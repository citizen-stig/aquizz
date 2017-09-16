from flask import request, redirect, url_for
from flask_admin.contrib.mongoengine import ModelView
from flask_security import current_user


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
    form_subdocuments = {
        'options': {
            'form_subdocuments': {
                None: {
                    'form_columns': ('value', 'is_correct')
                }
            }

        }
    }
