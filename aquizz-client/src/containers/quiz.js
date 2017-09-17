import { connect } from 'react-redux';
import Quiz from '../components/quiz';

const mapStateToProps = state => {
  console.log('Chaning...');
  console.log(state);
  return {
    questions: state.quiz.get('questions'),
  };
};

export default connect(mapStateToProps)(Quiz);
