import * as types from '../constants/actionTypes';
import * as api from '../services/api';

const __startQuiz = () => ({ type: types.START_QUIZ });
const __startQuizSuccess = (quizId, questions) => ({ type: types.START_QUIZ_SUCCESS, quizId, questions });
const __startQuizError = error => ({ type: types.START_QUIZ_ERROR, error});


export const startQuiz = playerName => {
  return d => {
    d(__startQuiz());
    return api.startQuiz(playerName)
      .then(response => d(__startQuizSuccess(response.body['id'], response.body['questions'])))
      .catch(err => d(__startQuizError(err)))
  }
};

const __sendAnswer = () => ({ type: types.SEND_ANSWER});
const __sendAnswerSuccess = (isCorrect, userSelected, correctOptions) => ({
  type: types.SEND_ANSWER_SUCCESS,
  isCorrect,
  userSelected,
  correctOptions,
});
const __sendAnswerError = error => ({ type: types.SEND_ANSWER_ERROR, error});

export const sendAnswer = (questionId, answer) => {
  return (d, s) => {
    const quizId = s().quiz.get('quiz');
    d(__sendAnswer());
    return api.sendAnswer(quizId, questionId, answer)
      .then(response => d(__sendAnswerSuccess(response.body['is_correct'], answer, response.body['correct_options'])))
      .catch(response => {
        d(__sendAnswerError('Something...'));
      });
    // TODO: add error catching;
  }
};

export const nextQuestion = () => ({ type: types.NEXT_QUESTION });
