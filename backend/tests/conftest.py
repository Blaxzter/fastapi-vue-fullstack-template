"""Shared fixtures for unit tests.

This module imports all fixtures from the fixtures/ subdirectory.
Fixtures are organized by domain for better maintainability:
- database.py: Database setup and session fixtures
- users.py: User fixtures (test_user, test_admin_user, etc.)
- projects.py: Project fixtures
- tasks.py: Task fixtures
- auth.py: Auth0 mock claims fixtures
- client.py: FastAPI app and HTTP client fixtures
"""

# Import all fixtures so they are available to tests
# ruff: noqa: F401
from tests.fixtures.auth import (
    mock_auth0_admin_claims,
    mock_auth0_claims,
    mock_auth0_claims_no_sub,
    mock_auth0_new_user_claims,
)
from tests.fixtures.client import app, as_admin, async_client
from tests.fixtures.database import db_session, test_db_setup, test_engine
from tests.fixtures.projects import test_project, test_project_without_owner
from tests.fixtures.tasks import multiple_test_tasks, test_task
from tests.fixtures.users import test_admin_user, test_inactive_user, test_user
