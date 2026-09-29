# CAT Prep Platform

Personalized CAT (Common Admission Test) preparation platform: blended mock tests (real PYQs + AI-generated questions) and AI-driven Personal Interview (PI) practice, built around a per-student weak-concept ledger and background-aware onboarding.

## What makes this different

- **Weak-concept ledger drives mock-test question weighting** from the first test onward, not just shown as a static chart.
- **Onboarding calibration before failure** — academic background (engineering/commerce/humanities) biases initial section weighting.
- **One dashboard, one trajectory** — mock-test performance and PI readiness surface together, not as two disconnected products.

See `Future Features.md` for what's deliberately deferred (WAT module, institute-specific PI personas, weak-area-to-PI fusion, real PYQ ingestion pipeline, real percentile calibration).

## Stack

FastAPI + SQLAlchemy + Alembic + PostgreSQL + Google Gemini (backend), React + Vite (frontend).

## Local development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # fill in GEMINI_API_KEYS, SECRET_KEY, DATABASE_URL
alembic upgrade head
python -m app.scripts.seed_cat_questions   # seeds ~30 hand-written PYQ-style questions
uvicorn app.main:app --reload   # http://localhost:8000, docs at /docs
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env            # VITE_API_BASE_URL=http://localhost:8000
npm run dev                     # http://localhost:5173
```

### Full stack (Docker)

```bash
cp backend/.env.example backend/.env   # fill in real values first
docker compose up --build
```

Starts Postgres, backend (`:8000`, runs Alembic migrations on boot), and frontend (`:3000`, nginx-served build) together.

## Repo layout

```
backend/app/
  api/        FastAPI routers (auth, cat_profile, cat_mock_tests, cat_pi, cat_weak_concepts, dashboard)
  models/     SQLAlchemy models
  schemas/    Pydantic request/response models
  services/   business logic + services/prompts/ (Gemini prompt builders)
  utils/      JWT + password hashing
  scripts/    seed_cat_questions.py
frontend/src/
  api/        one file per backend domain, built on a shared axios client
  context/    AuthContext, CatMockTestContext (survives navigation during test generation)
  pages/      routed pages
  router.jsx  centralized route definitions
```
