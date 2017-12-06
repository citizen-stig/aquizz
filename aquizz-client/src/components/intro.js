import React, {Component} from 'react';
import PropTypes from 'prop-types';

import Loader from './loader';

class Intro extends Component {
  static propTypes = {
    startQuiz: PropTypes.func.isRequired,
    isLoading: PropTypes.bool,
  }

  constructor(props) {
    super(props);
    this.state = {
      playerName: '',
    };
  }

  updateName = e => {
    this.setState({playerName: e.target.value})
  }

  submitForm = e => {
    e.preventDefault();
    this.props.startQuiz(this.state.playerName);
  }

  render() {
    return (<div className="row quiz-intro-container">
      {this.props.isLoading ?
        <Loader/> :
      <div className="col-12 text-center quiz-intro">
        <h1>Welcome!</h1>
        <p><small>Test your knowledge of extensively used acronyms!</small></p>
        <form onSubmit={this.submitForm} method="post">
          <div className="form-group">
            <label htmlFor="player-name">Enter your full name or login</label>
            <input type="text"
                   className="form-control"
                   id="player-name"
                   name="player-name"
                   onChange={this.updateName}
            />
          </div>
          <button type="submit" className="btn-lg btn-primary">Start Quiz</button>
        </form>
        <div className="alert intro-description" role="alert">
          <small>This quiz is highly subjective and doesn't claim to be ground truth for anything. Just enjoy.</small>
        </div>
      </div>
      }
    </div>);
  }
}

export default Intro;
