import { connect } from 'react-redux';
import App from '../components/app.js';


const mapStateToProps = state => {
  return {
    isLoading: state.quiz.get('isLoading'),
    quiz: state.quiz.get('questions').size > 0,
  };
};

export default connect(mapStateToProps, null)(App);


