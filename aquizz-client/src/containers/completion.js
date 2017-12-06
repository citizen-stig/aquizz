import { connect } from 'react-redux';
import Completion from '../components/completion';
import * as actions from '../actions/quiz';

const mapStateToProps = state => {
  const correctNumber = state.quiz.get('questions').filter(question => question.get('isCorrect')).size;
  const correctPercentage = (correctNumber / state.quiz.get('questions').size) * 100;
  return {correctNumber, correctPercentage};
};

const mapDispatchToProps = dispatch => {
  return {
    restartQuiz: () => dispatch(actions.restartQuiz())
  }
};


export default connect(mapStateToProps, mapDispatchToProps)(Completion);
