import React, {Component} from 'react';
import PropTypes from 'prop-types';
import cn from 'classnames';

class Question extends Component {
  static propTypes = {
    question: PropTypes.object.isRequired,
    selectOption: PropTypes.func,
  }

  render() {
    const isAnswered = this.props.question.get('isAnswered');
    const isCorrect = this.props.question.get('isCorrect');
    return (<div>
      <h1 className="text-center">{this.props.question.get('text')}</h1>
      <div className="row">
        {this.props.question.get('options').map(option => {
          const isUserSelected = isAnswered && this.props.question
            .get('userSelected') === option;
          const classes = cn('btn', 'btn-block', {
            'btn-secondary': !isAnswered,
            'btn-success': isAnswered && this.props.question.get('correctOptions')
              .findIndex(correctOption => correctOption === option) >= 0,
            'btn-danger': isAnswered && !isCorrect && isUserSelected,
          });
          return (
            <div key={option} className="col-xs-12 col-sm-6 option-container">
              <button className={classes} disabled={isAnswered}
                      onClick={() => this.props.selectOption(option)}>
                {option}
              </button>
            </div>);
        })}
      </div>
    </div>);
  }
}

export default Question;