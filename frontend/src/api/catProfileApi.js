import client from './client'

export function getCatProfile() {
  return client.get('/cat/profile').then((res) => res.data)
}

export function updateCatProfile({ cat_academic_background, cat_target_iims, cat_target_percentile }) {
  return client
    .put('/cat/profile', { cat_academic_background, cat_target_iims, cat_target_percentile })
    .then((res) => res.data)
}
