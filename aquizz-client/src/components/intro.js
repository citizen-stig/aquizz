import React, {Component} from 'react';
import PropTypes from 'prop-types';

class Intro extends Component {
  static propTypes = {
    startQuiz: PropTypes.func.isRequired,
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
                   placeholder="Optional"
                   onChange={this.updateName}
            />
          </div>
          <button type="submit" className="btn-lg btn-primary">Start Quiz</button>
        </form>
      </div>
    </div>);
  }
}

export default Intro;
