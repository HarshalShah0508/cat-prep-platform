import contextlib
import logging
import threading
import time
from typing import Any, Optional, Type, TypeVar

from google import genai
from google.genai import types
from pydantic import BaseModel

from app.core.config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

COOLDOWN_SECONDS = 60
DEFAULT_MODEL = "gemini-3.5-flash"

LANGFUSE_ENABLED = bool(settings.langfuse_public_key and settings.langfuse_secret_key)

if LANGFUSE_ENABLED:
    from openinference.instrumentation.google_genai import GoogleGenAIInstrumentor
    from langfuse import get_client as get_langfuse_client, propagate_attributes

    GoogleGenAIInstrumentor().instrument()
    get_langfuse_client()


class GeminiKeyManager:
    """Rotates across the configured GEMINI_API_KEYS, tracking a per-key cooldown when a
    key comes back rate-limited (429) or unavailable (503)."""

    def __init__(self, api_keys: Optional[list] = None) -> None:
        self._api_keys = api_keys if api_keys is not None else settings.gemini_api_keys
        if not self._api_keys:
            raise ValueError("No Gemini API keys configured")
        self._cooldown_until = {key: 0.0 for key in self._api_keys}
        self._clients: dict = {}
        self._cursor = 0
        self._cursor_lock = threading.Lock()

    def _client_for(self, api_key: str) -> "genai.Client":
        if api_key not in self._clients:
            # Without an explicit timeout, a single wedged connection can hang the
            # calling thread indefinitely (observed in practice: a background mock-test
            # generation task stuck for 7+ minutes on one call with no error ever
            # raised) - bound it so a stuck request surfaces as a retryable failure
            # instead of hanging the whole generation job.
            self._clients[api_key] = genai.Client(
                api_key=api_key,
                http_options=types.HttpOptions(timeout=60_000),
            )
        return self._clients[api_key]

    def _ordered_keys(self) -> list:
        """Round-robin the starting key each call so load actually spreads across all
        configured keys instead of always hammering the first one while it's healthy -
        keys still in cooldown are pushed to the end as a last-resort fallback."""
        num_keys = len(self._api_keys)
        with self._cursor_lock:
            start = self._cursor
            self._cursor = (self._cursor + 1) % num_keys
        rotated = self._api_keys[start:] + self._api_keys[:start]

        now = time.time()
        available = [k for k in rotated if self._cooldown_until.get(k, 0.0) <= now]
        cooling_down = [k for k in rotated if self._cooldown_until.get(k, 0.0) > now]
        return available + cooling_down

    def _mark_cooldown(self, api_key: str) -> None:
        self._cooldown_until[api_key] = time.time() + COOLDOWN_SECONDS

    def generate_content(
        self,
        prompt: Optional[str] = None,
        response_schema: Optional[Type[T]] = None,
        purpose: str = "",
        model: str = DEFAULT_MODEL,
        contents: Optional[Any] = None,
        user_id: Optional[int] = None,
    ) -> Any:
        """Generate content with Gemini, rotating across keys on rate-limit errors.

        `contents` overrides `prompt` when given - lets a multimodal call (e.g. a PDF
        `Part` alongside instruction text) go through the same rotating-key chokepoint
        instead of bypassing it.

        Returns the raw text response, or a parsed instance of `response_schema` when given.
        """
        last_error: Optional[Exception] = None
        keys_to_try = self._ordered_keys()[: len(self._api_keys)]
        request_contents = contents if contents is not None else prompt

        for api_key in keys_to_try:
            client = self._client_for(api_key)
            try:
                config = None
                if response_schema is not None:
                    config = types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=response_schema,
                    )

                trace_scope = (
                    propagate_attributes(
                        user_id=str(user_id) if user_id is not None else None,
                        metadata={"purpose": purpose},
                        tags=[purpose],
                    )
                    if LANGFUSE_ENABLED
                    else contextlib.nullcontext()
                )
                with trace_scope:
                    response = client.models.generate_content(
                        model=model,
                        contents=request_contents,
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
