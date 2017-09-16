from bson import ObjectId
import random

from flask import jsonify
from flask_restful import Resource, abort
from webargs.flaskparser import parser, use_args, use_kwargs
from marshmallow import fields, validate, Schema, ValidationError


from aquizz import models, exc

# API Endpoints
# /quiz
#   GET  => list of all past quizzes
#   POST => creates new quiz in database, returns quiz_id, and list of questions
# /quiz/<id>/
#   POST => validates answer


class ItemSchema(Schema):
    question_id = fields.String(required=True)
    answer = fields.String(required=True)


class QuizListResource(Resource):

    def get(self):
        return {
            'questions': [1, 2, 3]
        }

    def post(self):
        all_questions = list(models.Question.objects())
        quiz = models.Quiz()
        questions = []
        for question in random.sample(all_questions, 10):
            questions.append({
                'id': str(question.id),
                'text': question.text,
                'variants': [x.value for x in question.options]
            })
            item = models.Item(question=question)
            quiz.items.append(item)
        quiz.save()
        return {
            'id': str(quiz.id),
            'questions': questions,
        }


class QuizResource(Resource):

    @use_args(ItemSchema(strict=True))
    def post(self, args, quiz_id):
        quiz = models.Quiz.objects.get_or_404(pk=quiz_id)
        try:
            is_correct = quiz.check_answer(
                ObjectId(args['question_id']),
                args['answer'])
        except exc.QuizException as e:
            return abort(400, message=str(e))
        if is_correct is None:
            return abort(404, message='Question not found in quiz')
        return {'is_correct': is_correct}
