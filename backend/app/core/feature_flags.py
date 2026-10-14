"""Temporary kill-switch for AI (Gemini) powered features.

Flip AI_FEATURES_DISABLED to False (or delete this module and its call sites) once
Gemini traffic/quota pressure eases.
"""

AI_FEATURES_DISABLED = True

AI_DISABLED_MESSAGE = (
    "We're experiencing heavy traffic on our AI services right now, so this feature is "
    "temporarily disabled. Please try again later."
)
