import client from './client'

const BASE = '/cat/pyq'

export function getAvailablePyqPapers() {
  return client.get(`${BASE}/available`).then((res) => res.data)
}

export function startPyqPaper({ source_year, source_slot, sections }) {
  return client.post(`${BASE}/start`, { source_year, source_slot, sections }).then((res) => res.data)
}
