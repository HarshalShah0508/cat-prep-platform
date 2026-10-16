import { getCatProfile } from '../api/catProfileApi'

// New accounts have no CAT profile yet — send them to onboarding first.
// Shared by password login and Google login, which both land here after
// getting a token back.
export async function redirectAfterAuth(navigate, redirectTo) {
  try {
    const profile = await getCatProfile()
    if (profile && profile.cat_academic_background) {
      navigate(redirectTo || '/dashboard')
    } else {
      navigate('/onboarding')
    }
  } catch {
    navigate('/onboarding')
  }
}
