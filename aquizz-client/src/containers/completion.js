import { connect } from 'react-redux';
import Completion from '../components/completion';

const mapStateToProps = state => {
  const correctNumber = state.quiz.get('questions').filter(question => question.get('isCorrect')).size;
  const correctPercentage = (correctNumber / state.quiz.get('questions').size) * 100;
  return {correctNumber, correctPercentage};
};


export default connect(mapStateToProps)(Completion);
