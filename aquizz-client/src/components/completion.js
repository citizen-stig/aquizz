import React, {Component} from 'react';
import PropTypes from 'prop-types';
import cn from 'classnames';

const success_reactions = [
  'https://media.giphy.com/media/3o7TKtsBMu4xzIV808/giphy.gif',
  'https://media.giphy.com/media/pbuK5WWsRwpu8/giphy.gif',
  'https://media.giphy.com/media/iEXlNtAHe3mw/giphy.gif',
  'https://media.giphy.com/media/RIhNQOjGa39Ze/giphy.gif',
  'https://media.giphy.com/media/KvGkTDzBnY03m/giphy.gif',
];

const ok_reactions = [
  'https://media0.giphy.com/media/5hc2bkC60heU/giphy.gif',
  'https://media0.giphy.com/media/a3zqvrH40Cdhu/giphy.gif',
  'https://media2.giphy.com/media/iuXnKvwKtuqNq/giphy.gif',
  'https://media0.giphy.com/media/H7ZO0pGybYely/giphy.gif',
  'https://media0.giphy.com/media/NiyxeWm81N0cg/giphy.gif',
];

const failure_reactions = [
  'https://media.giphy.com/media/xT77Y36ijyuwn58bja/giphy.gif',
  'https://media2.giphy.com/media/oHYH3TF7Viq76/giphy.gif',
  'https://media3.giphy.com/media/BrEi59xsJqEWk/giphy.gif',
  'https://media2.giphy.com/media/3og0INyCmHlNylks9O/giphy.gif',
  'https://media2.giphy.com/media/U4VXRfcY3zxTi/giphy.gif',
];

const selectRandom = values => values[Math.floor(Math.random() * values.length)];

class Completion extends Component {
  static propTypes = {
    correctNumber: PropTypes.number,
    correctPercentage: PropTypes.number,
  }

  render() {
    let gif, shortMessage, longMessage, alertClass;
    if (this.props.correctPercentage >= 90) {
      gif = selectRandom(success_reactions);
      shortMessage = 'Well done!';
      longMessage = 'Great!!!!';
      alertClass = 'alert-success';
    } else if (this.props.correctPercentage < 90 && this.props.correctPercentage >= 70) {
      gif = selectRandom(ok_reactions);
      shortMessage = 'Heads up!';
      longMessage = 'Good.';
      alertClass = 'alert-info'
    } else {
      gif = selectRandom(failure_reactions);
      shortMessage = 'So close!';
      longMessage = 'Could be better.';
      alertClass = 'alert-warning'
    }
    return (<div className="text-center">

      <div className="row">
        <div className="col-12">
          <h1>Completed</h1>
          <p>Correct answers: <strong>{this.props.correctNumber} ({this.props.correctPercentage}%)</strong></p>
        </div>
      </div>
      <div className="row">
        <div className="col-12">
          <img className="rounded complete-reaction" src={gif} alt={shortMessage}/>
          <div className={cn('alert', 'complete-message', alertClass)} role="alert">
            <strong>{shortMessage}</strong> {longMessage}
          </div>
        </div>
      </div>
    </div>);
  }
}

export default Completion;
