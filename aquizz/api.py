import random

from bson import ObjectId
from flask_restful import Resource, abort
from marshmallow import fields, Schema
from webargs.flaskparser import use_args

from aquizz import models, exc


class NewQuizSchema(Schema):
    player_name = fields.String(required=False)


class ItemSchema(Schema):
    question_id = fields.String(required=True)
    answer = fields.String(required=True)


class QuizListResource(Resource):
    size = 10

    def get(self):
        return {
            'questions': [1, 2, 3]
        }

    @use_args(NewQuizSchema())
    def post(self, args):
        player_name = args.get('player_name', 'Anonymous')
        all_questions = list(models.Question.objects(__raw__={'$where': 'this.options.length >= 4'}))
        quiz = models.Quiz(player_name=player_name)
        questions = []
        if len(all_questions) < self.size:
            return abort(500)
        for question in random.sample(all_questions, self.size):
            options = [x.value for x in question.options]
            random.shuffle(options)
            questions.append({
                'id': str(question.id),
                'text': question.text,
                'options': options,
            })
            item = models.Item(question=question)
            quiz.items.append(item)
        quiz.save()
        return {
            'id': str(quiz.id),
            'questions': questions,
        }


class QuizResource(Resource):

    @use_args(ItemSchema())
    def post(self, args, quiz_id):
        quiz = models.Quiz.objects.get_or_404(pk=quiz_id)
        question_id = ObjectId(args['question_id'])
        try:
            is_correct = quiz.check_answer(question_id, args['answer'])
            quiz.check_if_completed()
        except exc.QuizException as e:
            return abort(400, message=str(e))
        if is_correct is None:
            return abort(404, message='Question not found in quiz')
        correct_options = quiz.get_correct_options(question_id)
        return {
            'is_correct': is_correct,
            'correct_options': [x.value for x in correct_options]
        }
