from fastapi import APIRouter, Depends

from app.api.deps import SessionDep, auth0
from sqlalchemy import text

router = APIRouter(prefix="/test", tags=["Test"])


@router.get("/")
async def your_endpoint(
    session: SessionDep, claims: dict = Depends(auth0.require_auth())
):
    """Your endpoint description"""
    # Your logic here
    print(claims)  # Example usage of claims

    # test the session dependency
    await session.exec(text("SELECT 1"))

    return {"message": "Hello from your endpoint!", "claims": claims}
