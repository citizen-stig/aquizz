import { connect } from 'react-redux'
import * as actions from '../actions/quiz'
import Intro from '../components/intro';

const mapStateToProps = state => {
  return {
    isLoading: state.quiz.get('isLoading'),
  };
};


const mapDispatchToProps = dispatch => {
  return {
    startQuiz: playerName => dispatch(actions.startQuiz(playerName))
  }
};

export default connect(mapStateToProps, mapDispatchToProps)(Intro);
