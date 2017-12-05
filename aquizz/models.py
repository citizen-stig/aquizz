from bson import ObjectId
from datetime import datetime
from flask_mongoengine import MongoEngine
from flask_security import UserMixin, RoleMixin, MongoEngineUserDatastore

from aquizz import exc

db = MongoEngine()


class Option(db.EmbeddedDocument):
    value = db.StringField(required=True)
    is_correct = db.BooleanField(default=False)

    def __str__(self):
        return self.value


class Question(db.Document):
    id = db.ObjectIdField(primary_key=True, default=ObjectId)
    text = db.StringField(required=True, unique=True)
    options = db.ListField(db.EmbeddedDocumentField(Option))

    def __str__(self):
        return self.text

    def get_correct_options(self):
        return (x for x in self.options if x.is_correct)

    def is_answer_correct(self, value):
        return value in (x.value for x in self.get_correct_options())


class Item(db.EmbeddedDocument):
    question = db.ReferenceField(Question, required=True)
    answer = db.StringField(required=False)
    points = db.IntField(min_value=0, max_value=100)
    answered_at = db.DateTimeField(required=False)

    def __str__(self):
        tick = ''
        if self.answer:
            is_correct = self.question.is_answer_correct(self.answer)
            tick = '✔ ' if is_correct else '✗ '
        return '{0}{1} => {2} @ {3} <br/>'.format(
            tick,
            self.question,
            self.answer,
            self.answered_at,
        )


class Quiz(db.Document):
    id = db.ObjectIdField(primary_key=True, default=ObjectId)
    started_at = db.DateTimeField(required=True, default=datetime.utcnow())
    finished_at = db.DateTimeField(required=False, default=None)
    player_name = db.StringField(required=False, default='Anonymous')
    items = db.ListField(db.EmbeddedDocumentField(Item))

    def check_answer(self, question_id: ObjectId, value: str):
        for item in self.items:
            if item.question.id == question_id:
                if item.answer:
                    raise exc.QuizException('Question already answered')
                item.answer = value
                item.answered_at = datetime.utcnow()
                item.save()
                return item.question.is_answer_correct(value)

    def get_correct_options(self, question_id):
        for item in self.items:
            if item.question.id == question_id:
                return item.question.get_correct_options()

    def check_if_completed(self):
        unanswered_questions = sum(1 for x in self.items if x.answered_at is None)
        is_completed = unanswered_questions == 0
        if is_completed and self.finished_at is None:
            self.finished_at = datetime.utcnow()
            self.save()


###################################
class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

    def __str__(self):
        return self.name


class User(UserMixin, db.Document):
    email = db.StringField(required=True, unique=True)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=lambda: [])

    def __str__(self):
        return self.email


user_datastore = MongoEngineUserDatastore(db, User, Role)
