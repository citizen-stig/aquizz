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
    return (<div className="row">
      <div className="col-12 text-center">
        <h1>Hello!</h1>
        <form onSubmit={this.submitForm} method="post">
          <div className="form-group">
            <label htmlFor="player-name">Enter your name</label>
            <input type="text"
                   className="form-control"
                   id="player-name"
                   name="player-name"
                   placeholder="optional"
                   onChange={this.updateName}
            />
          </div>
          <button type="submit" className="btn btn-primary">start quiz</button>
        </form>
      </div>
    </div>);
  }
}

export default Intro;
