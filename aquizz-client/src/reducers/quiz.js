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
  const currentQuestionIdx = state.get('currentQuestion', 0);
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
      const currentQuestion = state.getIn(['questions', currentQuestionIdx]).mergeDeep({
        isAnswered: true,
        isCorrect: action.isCorrect,
        correctOptions: action.correctOptions,
        userSelected: action.userSelected,
      });
      return state
        .mergeDeep({
          isLoading: false,
          error: null,
          completed: currentQuestionIdx === state.get('questions').size - 1,
        })
        .setIn(['questions', currentQuestionIdx], currentQuestion);
    case types.SEND_ANSWER_ERROR:
      return state.mergeDeep({
        isLoading: false,
        error: action.error,
      });
    case types.NEXT_QUESTION:
      return state.set('currentQuestion', currentQuestionIdx + 1);
    default:
      return state;
  }
}

