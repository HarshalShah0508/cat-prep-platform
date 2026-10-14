// TEMP: mirrors backend/app/core/feature_flags.py. Flip to false (and remove the
// disabled banners/guards at the call sites) once Gemini traffic/quota pressure eases.
export const AI_FEATURES_DISABLED = true

export const AI_DISABLED_MESSAGE =
  "We're experiencing heavy traffic on our AI services right now, so this feature is temporarily disabled. Please try again later."
