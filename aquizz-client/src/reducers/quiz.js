import { fromJS } from 'immutable';

import * as types from '../constants/actionTypes';

const initialState = fromJS({
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
      return state.set('isLoading', true);
    case types.START_QUIZ_SUCCESS:
      return state.mergeDeep({
        isLoading: false,
        currentQuestion: 0,
        questions: action.questions,
        playerName: action.playerName,
      });
    case types.START_QUIZ_ERROR:
      return state.mergeDeep({
        isLoading: false,
        error: action.error,
      });
    default:
      return state;
  }
}

