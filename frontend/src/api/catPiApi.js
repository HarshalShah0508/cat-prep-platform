import client from './client'

const BASE = '/cat/pi'

export function startPiSession() {
  return client.post(`${BASE}/start`).then((res) => res.data)
}

export function getPiSession(id) {
  return client.get(`${BASE}/${id}`).then((res) => res.data)
}

export function answerPiQuestion(id, { pi_session_question_id, answer_text }) {
  return client
    .post(`${BASE}/${id}/answer`, { pi_session_question_id, answer_text })
    .then((res) => res.data)
}

export function finishPiSession(id) {
  return client.post(`${BASE}/${id}/finish`).then((res) => res.data)
}
