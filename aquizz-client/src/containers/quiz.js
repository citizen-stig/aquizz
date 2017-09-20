import { connect } from 'react-redux';
import * as actions from '../actions/quiz'
import Quiz from '../components/quiz';

const mapStateToProps = state => {
  return {
    isLoading: state.quiz.get('isLoading'),
    currentQuestion: state.quiz.getIn(['questions', state.quiz.get('currentQuestion')]),
    completed: state.quiz.get('completed'),
  };
};

const mapDispatchToProps = dispatch => {
  return {
    sendAnswer: (questionId, answer) => dispatch(actions.sendAnswer(questionId, answer))
  }
};

export default connect(mapStateToProps, mapDispatchToProps)(Quiz);
