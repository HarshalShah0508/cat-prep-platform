import client from './client'

export function getDashboard() {
  return client.get('/dashboard').then((res) => res.data)
}
