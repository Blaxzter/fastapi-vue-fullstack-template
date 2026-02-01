# AI README

This document is for AI agents and contributors who need fast, accurate context and best practices for this repo. It combines the key points from the project READMEs and adds extra guidance that would be too long for the main docs.

## Quick Start (local)

Option A: Docker Compose (recommended for full stack)

```bash
docker compose watch
```

Option B: Run services locally

```bash
# Backend
cd backend
uv sync
fastapi dev app/main.py

# Frontend (separate terminal)
cd frontend
pnpm install
pnpm dev
```

Useful local URLs:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- OpenAPI docs: http://localhost:8000/docs

## Tech Stack (source of truth)

Backend

- FastAPI + Pydantic v2
- SQLModel (async SQLAlchemy) + Alembic
- PostgreSQL (psycopg + asyncpg)
- Auth0 integration via auth0-fastapi-api + JWT (pyjwt)
- httpx for outbound HTTP
- Tooling: uv, Ruff, Mypy, Pytest, pre-commit

Frontend

- Vue 3 + TypeScript + Vite
- Tailwind CSS v4
- shadcn-vue patterns (reka-ui components)
- Pinia + Vue Router
- Vee-Validate + Zod
- Vue I18n, VueUse
- OpenAPI client via @hey-api/openapi-ts
- Playwright, ESLint, Prettier
- pnpm

Infra

- Docker Compose, Traefik, GitHub Actions

## Repo Map

- `backend/` FastAPI app
- `backend/app/api/routes/` API endpoints (one file per domain)
- `backend/app/crud/` CRUD helpers (CRUDBase + per-model classes)
- `backend/app/models/` SQLModel models and base classes
- `backend/app/schemas/` Pydantic schemas (create/read/update)
- `backend/app/logic/` business logic/services
- `backend/app/core/` config, security, and infrastructure
- `frontend/src/components/ui/` shadcn-vue style UI components
- `frontend/src/client/` auto-generated API client (do not hand-edit)

## Environment Configuration

- Root `.env` is used by Docker Compose. See `.env.example` for required keys.
- Frontend uses `frontend/.env` (see `frontend/.env.example`).
- Auth0 is required for local auth flows (both backend + frontend).

Backend Auth0 variables (root `.env`):

- `AUTH0_DOMAIN`
- `AUTH0_AUDIENCE`
- `AUTH0_CLIENT_ID`
- `AUTH0_CLIENT_SECRET`

Frontend Auth0 variables (`frontend/.env`):

- `VITE_AUTH0_DOMAIN`
- `VITE_AUTH0_CLIENT_ID`
- `VITE_AUTH0_API_AUDIENCE`
- `VITE_AUTH0_CALLBACK_URL`

## Backend Development Patterns

When adding a new feature:

1. Model: add a SQLModel in `backend/app/models/`.
2. Schemas: add create/read/update Pydantic schemas in `backend/app/schemas/`.
3. CRUD: extend `CRUDBase` in `backend/app/crud/`.
4. Routes: add a new router in `backend/app/api/routes/`.
5. Register the router in `backend/app/api/main.py`.
6. (Optional) Add service functions in `backend/app/logic/`.
7. Create Alembic migrations and commit them.

Auth pattern (per routes README):

- Use `CurrentUser` (from `app.api.deps`) for database-related endpoints that need:
    - User validation (exists in database, is active)
    - Role-based access control
    - Database user object access
- Use `CurrentSuperuser` for admin-only endpoints (e.g., delete, create users)
- Use both `CurrentUser` and `claims: dict = Depends(auth0.require_auth())` when you need:
    - Database validation AND Auth0 profile data (e.g., `/me` endpoints)
- Use `auth0.require_auth()` alone only for Auth0-specific operations without database requirements

Database migrations:

```bash
# inside backend container or backend venv
alembic revision --autogenerate -m "Add <feature>"
alembic upgrade head
```

Testing:

```bash
bash ./scripts/test.sh
```

Linting:

```bash
uv run ruff check .
uv run mypy .
```

## Frontend Development Patterns

- Prefer UI primitives in `src/components/ui/` (shadcn-vue style).
- Keep routes in `src/router/` and feature views in `src/views/`.
- Use Pinia stores in `src/stores/` for app state.
- Add Zod schemas + Vee-Validate for forms.

Regenerate the API client when backend OpenAPI changes:

```bash
cd frontend
pnpm run generate-client
```

Testing and linting:

```bash
pnpm test:e2e
pnpm lint
pnpm format
```

## Cross-Cutting Conventions

- API base path is `/api/v1` (see `backend/app/core/config.py`).
- Keep schemas, CRUD, routes aligned; avoid logic in routers when it belongs in services.
- Use typed Pydantic schemas for all request/response bodies.
- Do not edit generated client code in `frontend/src/client/`.
- Prefer small, focused route modules with clear tags and prefixes.

## Gotchas

- Root `.env` values power Docker Compose services. Restart the stack after changes.
- The frontend expects `VITE_API_SERVER_URL` to include `/api/v1`.
- If you change models, create and apply Alembic migrations.

## Where to Read More

- `README.md` (root)
- `backend/README.md`
- `frontend/README.md`
- `development.md`
- `deployment.md`
