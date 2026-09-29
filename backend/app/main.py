from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api import auth, cat_mock_tests, cat_pi, cat_profile, cat_weak_concepts, dashboard
from app.core.config import settings
from app.core.rate_limiter import limiter

app = FastAPI(title="CAT Prep Platform API")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(cat_profile.router)
app.include_router(cat_mock_tests.router)
app.include_router(cat_pi.router)
app.include_router(cat_weak_concepts.router)
app.include_router(dashboard.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
