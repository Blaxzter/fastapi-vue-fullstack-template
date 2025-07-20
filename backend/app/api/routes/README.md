# API Routes

This directory is where you should create your FastAPI route modules to organize your application's REST API endpoints.

## Route Structure Guidelines

Each route file should follow this structure:

```python
from fastapi import APIRouter
from app.api.deps import SessionDep, CurrentUser

router = APIRouter(prefix="/your-prefix", tags=["your-tag"])

@router.get("/")
async def your_endpoint(session: SessionDep, current_user: CurrentUser):
    """Your endpoint description"""
    # Your logic here
    pass
```

## Essential Route Files to Create

### `login.py` (Required)

Authentication endpoints for user login and token management.

**Recommended Endpoints:**

-   `POST /login/access-token` - User authentication (OAuth2 password bearer)
-   `POST /login/test-token` - Validate token
-   `POST /login/recover-password` - Password recovery
-   `POST /login/reset-password` - Password reset

### `users.py` (Recommended)

User management endpoints.

**Typical Endpoints:**

-   `GET /users/me` - Get current user profile
-   `PATCH /users/me` - Update profile
-   `PATCH /users/me/password` - Change password
-   `POST /users/signup` - User registration
-   Admin endpoints for user management (if needed)

### Your Domain-Specific Routes

Create additional route files based on your application's needs:

-   `products.py` for e-commerce
-   `posts.py` for blog/social features
-   `orders.py` for order management
-   `analytics.py` for reporting endpoints
-   etc.

## Best Practices

### Route Organization

-   One route file per logical domain/resource
-   Use descriptive prefixes and tags
-   Group related endpoints together
-   Keep authentication logic in `login.py`

### Authentication Patterns

-   Use `CurrentUser` dependency for authenticated endpoints
-   Use `get_current_active_superuser` for admin-only endpoints
-   Implement proper error handling with HTTPException

### Common Dependencies

-   `SessionDep` for database operations
-   `CurrentUser` for authenticated routes
-   Custom dependencies for specific validation logic

### Response Models

-   Define Pydantic models for request/response validation
-   Use appropriate HTTP status codes
-   Include proper error responses

## Registration

Remember to register your routes in `api/main.py`:

```python
from app.api.routes import login, users, your_routes

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(your_routes.router)
```

This ensures your routes are included in the main application with the API version prefix.
