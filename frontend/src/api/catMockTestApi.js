import client from './client'

const BASE = '/cat/mock-tests'

export function startMockTest({
  test_type,
  sections,
  question_source,
  pyq_source_year,
  pyq_source_slot,
  topics,
  question_style,
  question_count,
}) {
  return client
    .post(`${BASE}/start`, {
      test_type,
      sections,
      question_source,
      pyq_source_year,
      pyq_source_slot,
      topics,
      question_style,
      question_count,
    })
    .then((res) => res.data)
}

export function getTopicOptions(section) {
  return client.get(`${BASE}/topic-options`, { params: { section } }).then((res) => res.data)
}

export function getMockTestStatus(id) {
  return client.get(`${BASE}/${id}/status`).then((res) => res.data)
}

export function getMockTest(id) {
  return client.get(`${BASE}/${id}`).then((res) => res.data)
}

export function startSection(id, section) {
  return client.post(`${BASE}/${id}/sections/${section}/start`).then((res) => res.data)
}

export function submitSectionAnswers(id, section, answers) {
  return client
    .post(`${BASE}/${id}/sections/${section}/answers`, { answers })
    .then((res) => res.data)
}

export function submitMockTest(id) {
  return client.post(`${BASE}/${id}/submit`).then((res) => res.data)
}

export function getMockTestResults(id) {
  return client.get(`${BASE}/${id}/results`).then((res) => res.data)
}
