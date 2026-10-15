import client from './client'

const BASE = '/cat/study-plan'

export function generateStudyPlan({ source, session_id }) {
  return client.post(`${BASE}/generate`, { source, session_id }).then((res) => res.data)
}

export function getStudyPlan() {
  return client.get(BASE).then((res) => res.data)
}
