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

    def is_answer_correct(self, value):
        correct_options = [x.value for x in self.options if x.is_correct]
        return value in correct_options


class Item(db.EmbeddedDocument):
    question = db.ReferenceField(Question, required=True)
    # chosen_variants = db.ListField(db.EmbeddedDocumentField(Variant))
    answer = db.StringField(required=False)
    points = db.IntField(min_value=0, max_value=100)


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
                item.save()
                return item.question.is_answer_correct(value)


##########################################
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
