import React, {Component} from 'react';
import PropTypes from 'prop-types';

import Question from './question';

class Quiz extends Component {
  static propTypes = {
    questions: PropTypes.object,
  }

  constructor(props) {
    super(props);
    this.state = {
      currentQuestion: 0,
    }
  }

  handleSelectedOption = option => {
    console.log('aaaa: ' + option);
    this.setState({
      currentQuestion: this.state.currentQuestion + 1
    });
  }

  render() {
    if (this.state.currentQuestion >= this.props.questions.size) {
      return (<p>Completed!</p>);
    }
    const question = this.props.questions.get(this.state.currentQuestion);
    return (<div>
        <p>Quesion: {this.state.currentQuestion + 1}</p>
        <Question
          key={question.get('text')}
          questionText={question.get('text')}
          options={question.get('options')}
          selectOption={this.handleSelectedOption}
        />
      </div>
    );
  }
}

export default Quiz;