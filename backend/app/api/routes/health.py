from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from app.api.deps import DBDep

router = APIRouter(tags=["Health"])


@router.get("/healthz")
async def health_check():
    """
    Liveness probe - checks if the application is running.
    Returns 200 OK if the service is alive.
    """
    return {"status": "ok"}


@router.get("/readyz")
async def readiness_check(db: DBDep):
    """
    Readiness probe - checks if the application is ready to serve requests.
    Includes database connectivity check.
    Returns 200 OK if the service is ready, 503 if not ready.
    """
    try:
        # Check database connectivity
        await db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service not ready: database connection failed - {str(e)}",
        ) from e
