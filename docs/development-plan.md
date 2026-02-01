# Development Plan (TODO)

## Phase 1 — Starter Product Slice
- [ ] Add a real example domain (Projects/Tasks) with full CRUD, pagination, filter, sort.
- [ ] Add backend models, schemas, CRUD helpers, routes, and Alembic migrations for the example domain.
- [ ] Add frontend list + create/edit form views for the example domain, wired to the generated API client.
- [ ] Add seed data and a reset workflow (script or CLI) to populate a demo dataset.

## Phase 2 — Reliability + Consistency
- [ ] Add `/healthz` and `/readyz` endpoints; include DB connectivity check for readiness.
- [ ] Standardize API error response shape (problem-details style) and document it.
- [ ] Normalize API errors on the frontend with a shared utility and consistent toast/messages.

## Phase 3 — Auth + Permissions Example
- [ ] Add a roles/permissions example using Auth0 claims (admin vs user).
- [ ] Enforce role-based access in API routes (admin-only and user-only examples).
- [ ] Add frontend route guards + conditional UI for role-based access.

## Phase 4 — Testing + DX
- [ ] Add backend unit tests for CRUD + auth dependencies with fixtures.
- [ ] Add Playwright e2e smoke test for login → list → create → edit → delete flow.
- [ ] Add a `justfile` or `make` tasks for common dev actions (lint/test/migrate/seed).

## Phase 5 — Observability + Ops
- [ ] Add structured logging with a request ID middleware.
- [ ] Add optional OpenTelemetry hooks (backend).
- [ ] Add frontend error boundary + Sentry/RUM wiring to match backend Sentry.
- [ ] Add a background job example (email/notification) with a lightweight queue.
