import * as types from '../constants/actionTypes';
import * as api from '../services/api';

const __startQuiz = () => ({ type: types.START_QUIZ });
const __startQuizSuccess = questions => ({ type: types.START_QUIZ_SUCCESS, questions });
const __startQuizError = error => ({ type: types.START_QUIZ_ERROR, error});


export const startQuiz = playerName => {
  return d => {
    d(__startQuiz());
    return api.startQuiz(playerName)
      .then(response => d(__startQuizSuccess(response.body.questions)))
      .catch(err => d(__startQuizError(err)))}
};

export const sendAnswer = (questionId, answer) => {
  return null;
};

