import React, {Component} from 'react';
import PropTypes from 'prop-types';

class Question extends Component {
  static propTypes = {
    questionText: PropTypes.string.isRequired,
    options: PropTypes.object,
    selectOption: PropTypes.func,
  }

  render() {
    return (<div>
      <p className="text-center">{this.props.questionText}</p>
      <div className="row">
        {this.props.options.map(option => {
          return (
            <div key={option} className="col-xs-12 col-sm-6 option-container">
              <button className="btn btn-secondary btn-block"
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