from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api import (
    auth,
    cat_mock_tests,
    cat_pi,
    cat_profile,
    cat_pyq,
    cat_resume,
    cat_study_plan,
    cat_weak_concepts,
    dashboard,
)
from app.core.config import settings
from app.core.rate_limiter import limiter
from app.services.gemini_key_manager import LANGFUSE_ENABLED


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if LANGFUSE_ENABLED:
        from langfuse import get_client

        get_client().flush()


app = FastAPI(title="CAT Prep Platform API", lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list({settings.frontend_origin, "http://localhost:3000", "http://localhost:5173"}),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(cat_profile.router)
app.include_router(cat_mock_tests.router)
app.include_router(cat_pyq.router)
app.include_router(cat_pi.router)
app.include_router(cat_resume.router)
app.include_router(cat_weak_concepts.router)
app.include_router(cat_study_plan.router)
app.include_router(dashboard.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
