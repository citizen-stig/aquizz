import { fromJS } from 'immutable';

import * as types from '../constants/actionTypes';

const initialState = fromJS({
  quiz: null,
  completed: false,
  playerName: null,
  questions: [],
  currentQuestion: null,
  isLoading: false,
  error: null,
});

export default (state = initialState, action) => {
  switch (action.type) {
    case types.START_QUIZ:
      return state.mergeDeep({
        isLoading: true,
        error: null,
      });
    case types.START_QUIZ_SUCCESS:
      return state.mergeDeep({
        isLoading: false,
        currentQuestion: 0,
        questions: action.questions,
        playerName: action.playerName,
        quiz: action.quizId,
      });
    case types.START_QUIZ_ERROR:
      return state.mergeDeep({
        isLoading: false,
        error: action.error,
      });
    case types.SEND_ANSWER:
      return state.mergeDeep({
        isLoading: true,
        error: null,
      });
    case types.SEND_ANSWER_SUCCESS:
      const currentQuestion = state.get('currentQuestion');
      return state
        .mergeDeep({
          isLoading: false,
          error: null,
        })
        .setIn(['questions', currentQuestion, 'isCorrect'], action.isCorrect)
        .mergeDeep({
          currentQuestion: currentQuestion + 1,
          completed: currentQuestion === state.get('questions').size - 1,
        });

    case types.SEND_ANSWER_ERROR:
      return state.mergeDeep({
        isLoading: false,
        error: action.error,
      });
    default:
      return state;
  }
}

