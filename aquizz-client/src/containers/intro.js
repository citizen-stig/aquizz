import { connect } from 'react-redux'
import * as actions from '../actions/quiz'
import Intro from '../components/intro';


const mapDispatchToProps = dispatch => {
  return {
    startQuiz: playerName => dispatch(actions.startQuiz(playerName))
  }
};

export default connect(null, mapDispatchToProps)(Intro);
