import logging
import time
from typing import Any, Optional, Type, TypeVar

from google import genai
from google.genai import types
from pydantic import BaseModel

from app.core.config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

COOLDOWN_SECONDS = 60
DEFAULT_MODEL = "gemini-2.0-flash"


class GeminiKeyManager:
    """Rotates across the configured GEMINI_API_KEYS, tracking a per-key cooldown when a
    key comes back rate-limited (429) or unavailable (503)."""

    def __init__(self, api_keys: Optional[list] = None) -> None:
        self._api_keys = api_keys if api_keys is not None else settings.gemini_api_keys
        if not self._api_keys:
            raise ValueError("No Gemini API keys configured")
        self._cooldown_until = {key: 0.0 for key in self._api_keys}
        self._clients: dict = {}

    def _client_for(self, api_key: str) -> "genai.Client":
        if api_key not in self._clients:
            self._clients[api_key] = genai.Client(api_key=api_key)
        return self._clients[api_key]

    def _ordered_keys(self) -> list:
        now = time.time()
        available = [k for k in self._api_keys if self._cooldown_until.get(k, 0.0) <= now]
        cooling_down = [k for k in self._api_keys if self._cooldown_until.get(k, 0.0) > now]
        return available + cooling_down

    def _mark_cooldown(self, api_key: str) -> None:
        self._cooldown_until[api_key] = time.time() + COOLDOWN_SECONDS

    def generate_content(
        self,
        prompt: str,
        response_schema: Optional[Type[T]] = None,
        purpose: str = "",
        model: str = DEFAULT_MODEL,
    ) -> Any:
        """Generate content with Gemini, rotating across keys on rate-limit errors.

        Returns the raw text response, or a parsed instance of `response_schema` when given.
        """
        last_error: Optional[Exception] = None
        keys_to_try = self._ordered_keys()[: len(self._api_keys)]

        for api_key in keys_to_try:
            client = self._client_for(api_key)
            try:
                config = None
                if response_schema is not None:
                    config = types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=response_schema,
                    )

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=config,
                )

                if response_schema is not None:
                    parsed = getattr(response, "parsed", None)
                    if parsed is not None:
                        return parsed
                    return response_schema.model_validate_json(response.text)

                return response.text

            except Exception as exc:  # noqa: BLE001 - need to inspect any provider error
                message = str(exc)
                status_code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
                is_rate_limited = (
                    status_code in (429, 503)
                    or "429" in message
                    or "503" in message
                    or "RESOURCE_EXHAUSTED" in message
                    or "UNAVAILABLE" in message
                )
                if is_rate_limited:
                    logger.warning("Gemini key rate-limited during '%s': %s", purpose, message)
                    self._mark_cooldown(api_key)
                else:
                    logger.error("Gemini call failed during '%s': %s", purpose, message)
                last_error = exc
                continue

        raise RuntimeError(
            f"All Gemini API keys exhausted or failing for purpose='{purpose}'"
        ) from last_error


gemini_key_manager = GeminiKeyManager()
