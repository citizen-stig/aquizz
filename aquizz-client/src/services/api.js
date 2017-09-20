import req from 'superagent';


const API_PATH = 'http://localhost:5000/api/v1';

export const startQuiz = playerName => {
  console.log('Player name not used for now: ' + playerName);
  return req.post(`${API_PATH}/quiz`);
};

export const sendAnswer = (quizId, questionId, answer) => {
  return req.post(`${API_PATH}/quiz/${quizId}`).send({question_id: questionId, answer});
};
