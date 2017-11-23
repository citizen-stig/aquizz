import req from 'superagent';


const API_PATH = 'http://localhost:5000/api/v1';

export const startQuiz = playerName => {
  return req.post(`${API_PATH}/quiz`).send({player_name: playerName});
};

export const sendAnswer = (quizId, questionId, answer) => {
  return req.post(`${API_PATH}/quiz/${quizId}`).send({question_id: questionId, answer});
};
