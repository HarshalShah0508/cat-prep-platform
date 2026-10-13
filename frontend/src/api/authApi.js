import client from './client'

export function signup({ email, password, username }) {
  return client.post('/auth/signup', { email, password, username }).then((res) => res.data)
}

export function login({ email, password }) {
  return client.post('/auth/login', { email, password }).then((res) => res.data)
}
