# Backend Unit Tests

This directory contains comprehensive unit tests for the backend application, focusing on CRUD operations and authentication dependencies.

## Test Structure

Tests are organized into subdirectories that mirror the backend application structure:

- **conftest.py** - Shared fixtures including database setup, test users, projects, and tasks
- **crud/** - CRUD operation tests
  - `test_user.py` - Tests for User CRUD operations
  - `test_project.py` - Tests for Project CRUD operations
  - `test_task.py` - Tests for Task CRUD operations
- **api/** - API and dependency tests
  - `test_deps.py` - Tests for authentication dependencies and role-based access control

## Running Tests

### Run all tests

```bash
cd backend
bash ./scripts/test.sh
```

Or with uv directly:

```bash
cd backend
uv run pytest
```

### Run specific test file

```bash
uv run pytest tests/crud/test_user.py
```

### Run specific test class or function

```bash
uv run pytest tests/crud/test_user.py::TestUserCRUD::test_create_user
```

### Run with verbose output

```bash
uv run pytest -v
```

### Run with coverage report

```bash
uv run coverage run --source=app -m pytest
uv run coverage report --show-missing
uv run coverage html
```

## Test Database

Tests use a separate PostgreSQL database (`app_test`) with the same Docker PostgreSQL instance as development. Each test session:

- Creates the test database
- Runs Alembic migrations to set up the schema
- Each test function gets a fresh transaction that is rolled back after the test
- Drops the test database after all tests complete

This ensures tests use the exact same database engine and schema as production.

## Fixtures

### Database Fixtures

- `test_engine` - Creates a test database engine
- `db_session` - Provides an async database session with automatic rollback

### User Fixtures

- `test_user` - Regular active user
- `test_admin_user` - Admin user with admin role
- `test_inactive_user` - Inactive user for testing access control

### Project Fixtures

- `test_project` - Project owned by test_user
- `test_project_without_owner` - Project without an owner

### Task Fixtures

- `test_task` - Single task for test_project
- `multiple_test_tasks` - Five tasks with varying properties

### Mock Auth0 Fixtures

- `mock_auth0_claims` - Claims for existing test_user
- `mock_auth0_admin_claims` - Claims for admin user
- `mock_auth0_new_user_claims` - Claims for new user (not in DB)
- `mock_auth0_claims_no_sub` - Invalid claims without 'sub'

## Test Coverage

The test suite covers:

### CRUD Operations

- Creating records
- Reading single and multiple records
- Updating records (full and partial updates)
- Deleting records
- Pagination and filtering
- Search functionality
- Sorting (ascending/descending)
- Counting filtered results
- 404 error handling

### Authentication & Authorization

- User creation on first login
- Existing user retrieval
- Role-based access control
- Active/inactive user handling
- Missing authentication payload errors
- CurrentUser and CurrentSuperuser dependencies

## Adding New Tests

When adding new tests:

1. Place tests in the appropriate subdirectory:
   - `tests/crud/` for CRUD operation tests
   - `tests/api/` for API endpoint and dependency tests
   - Create new subdirectories as needed (e.g., `tests/logic/` for business logic tests)
2. Use the provided fixtures from conftest.py
3. Mark async tests with `@pytest.mark.asyncio`
4. Organize tests into classes for better grouping
5. Use descriptive test names that explain what is being tested
6. Test both success and failure cases
7. Test edge cases (empty lists, None values, etc.)

Example:

```python
@pytest.mark.asyncio
class TestMyFeature:
    """Test suite for my feature."""

    async def test_feature_success(self, db_session: AsyncSession):
        """Test successful feature execution."""
        # Arrange
        # Act
        # Assert
        pass

    async def test_feature_failure(self, db_session: AsyncSession):
        """Test feature handles errors correctly."""
        # Arrange
        # Act & Assert
        with pytest.raises(HTTPException):
            # Code that should raise
            pass
```

## Dependencies

Required test dependencies (in pyproject.toml):

- `pytest` - Test framework
- `pytest-asyncio` - Async test support
- `coverage` - Test coverage reporting

Tests use the same database driver as production:

- `asyncpg` - PostgreSQL async driver
- `psycopg[binary]` - PostgreSQL driver

## CI/CD Integration

Requires PostgreSQL instance (use Docker in CI)

- Fast execution (typically < 1 minute for full suite)
- Requires standard environment variables (POSTGRES_SERVER, etc.)
- Deterministic results (no flaky tests)
- Automatic database cleanupry database)
- Fast execution (typically < 1 minute for full suite)
- No environment variables needed for basic tests
- Deterministic results (no flaky tests)
