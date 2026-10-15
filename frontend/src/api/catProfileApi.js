import client from './client'

export function getCatProfile() {
  return client.get('/cat/profile').then((res) => res.data)
}

export function updateCatProfile({
  cat_academic_background,
  cat_years_experience_band,
  cat_current_company,
  cat_target_percentile_min,
  cat_target_percentile_max,
}) {
  return client
    .put('/cat/profile', {
      cat_academic_background,
      cat_years_experience_band,
      cat_current_company,
      cat_target_percentile_min,
      cat_target_percentile_max,
    })
    .then((res) => res.data)
}
