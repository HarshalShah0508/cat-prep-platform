import client from './client'

const BASE = '/cat/pi'

export function startPiSession(resumeId) {
  return client.post(`${BASE}/start`, { resume_id: resumeId ?? null }).then((res) => res.data)
}

export function getPiSession(id) {
  return client.get(`${BASE}/${id}`).then((res) => res.data)
}

export function answerPiQuestion(id, { pi_session_question_id, answer_text, delivery_signals }) {
  return client
    .post(`${BASE}/${id}/answer`, { pi_session_question_id, answer_text, delivery_signals })
    .then((res) => res.data)
}

export function generatePiFollowUp(sessionId, answerId) {
  return client.post(`${BASE}/${sessionId}/answers/${answerId}/follow-up`).then((res) => res.data)
}

export function finishPiSession(id) {
  return client.post(`${BASE}/${id}/finish`).then((res) => res.data)
}

export function getPiSessionResults(id) {
  return client.get(`${BASE}/${id}/results`).then((res) => res.data)
}

export function submitPiSessionFeedback(id, payload) {
  return client.post(`${BASE}/${id}/feedback`, payload).then((res) => res.data)
}

export function submitPiSurvey(id, payload) {
  return client.post(`${BASE}/${id}/survey`, payload).then((res) => res.data)
}
