import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Intro from '../containers/intro';
import Quiz from '../containers/quiz';


class App extends Component {
  static propTypes = {
    quiz: PropTypes.bool,
  }

  render() {
    return (
      <div className="aquizz-app">
          {this.props.quiz ? <Quiz/> : <Intro/>}
      </div>
    );
  }
}

export default App;
