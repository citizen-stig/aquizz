import React, {Component} from 'react';
import PropTypes from 'prop-types';

import Question from './question';
import Loader from './loader';

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
      return (<p>Completed!</p>);
    }
    return (<div>
        {this.props.isLoading ? <Loader/> : null}
        <Question
          key={this.props.currentQuestion.get('text')}
          questionText={this.props.currentQuestion.get('text')}
          options={this.props.currentQuestion.get('options')}
          selectOption={this.handleSelectedOption}
        />
      </div>
    );
  }
}

export default Quiz;