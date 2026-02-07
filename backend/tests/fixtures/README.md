# Test Fixtures

This directory contains organized test fixtures for the FastAPI application.

## Structure

Fixtures are organized by domain for better maintainability and easier navigation:

### `database.py`

Database setup and session fixtures:

- `test_db_setup` - Sets up the test database (session scope)
- `test_engine` - Creates a test database engine
- `db_session` - Creates a test database session with transaction rollback

### `users.py`

User-related fixtures:

- `test_user` - Regular test user (non-admin)
- `test_admin_user` - Admin test user
- `test_inactive_user` - Inactive test user

### `projects.py`

Project-related fixtures:

- `test_project` - Test project owned by `test_user`
- `test_project_without_owner` - Orphan project without an owner

### `tasks.py`

Task-related fixtures:

- `test_task` - Single test task in `test_project`
- `multiple_test_tasks` - List of 5 test tasks in `test_project`

### `auth.py`

Auth0 mock claims fixtures:

- `mock_auth0_claims` - Standard Auth0 JWT claims
- `mock_auth0_admin_claims` - Admin Auth0 JWT claims
- `mock_auth0_new_user_claims` - New user Auth0 JWT claims
- `mock_auth0_claims_no_sub` - Auth0 claims without sub field

### `client.py`

FastAPI app and HTTP client fixtures:

- `app` - FastAPI app with dependency overrides for testing
- `async_client` - Async HTTP client for making requests
- `as_admin` - Context fixture to temporarily switch the current user to admin

## Usage

All fixtures are automatically imported via `conftest.py` and are available to any test file in the `tests/` directory.

Example:

```python
async def test_something(
    async_client: AsyncClient,
    db_session: AsyncSession,
    test_user: User,
):
    # Test code here
    pass
```

## Adding New Fixtures

When adding new fixtures:

1. Add them to the appropriate domain file (or create a new one if needed)
2. Import them in `conftest.py` to make them available to tests
3. Update this README with the new fixture name and description
