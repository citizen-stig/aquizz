import React, {Component} from 'react';
import PropTypes from 'prop-types';

import Question from './question';
import Loader from './loader';
import Completion from '../containers/completion';

class Quiz extends Component {
  static propTypes = {
    isLoading: PropTypes.bool,
    currentQuestion: PropTypes.object,
    completed: PropTypes.bool,
    sendAnswer: PropTypes.func.isRequired,
  }

  handleSelectedOption = option => {
    this.props.sendAnswer(this.props.currentQuestion.get('id'), option);
  }

  render() {
    if (this.props.completed) {
      return (<Completion/>);
    }
    return (<div>
        {this.props.isLoading ? <Loader/> : null}
        <Question
          key={this.props.currentQuestion.get('id')}
          question={this.props.currentQuestion}
          selectOption={this.handleSelectedOption}
        />
        {this.props.currentQuestion.get('isAnswered') &&
          <button className="btn btn-warning btn-block btn-lg" onClick={this.props.nextQuestion}>Next</button>}
      </div>
    );
  }
}

export default Quiz;