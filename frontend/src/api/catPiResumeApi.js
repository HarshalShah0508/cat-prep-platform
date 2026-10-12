import client from './client'

const BASE = '/cat/resume'

export function getResumes() {
  return client.get(BASE).then((res) => res.data)
}

export function uploadResume(file) {
  const formData = new FormData()
  formData.append('file', file)
  return client
    .post(`${BASE}/upload`, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    .then((res) => res.data)
}

export function deleteResume(resumeId) {
  return client.delete(`${BASE}/${resumeId}`).then((res) => res.data)
}
