import client from './client'

const BASE = '/cat/weak-concepts'

export function getWeakConcepts() {
  return client.get(BASE).then((res) => res.data)
}

export function practiceWeakConcept(id) {
  return client.post(`${BASE}/${id}/practice`).then((res) => res.data)
}
