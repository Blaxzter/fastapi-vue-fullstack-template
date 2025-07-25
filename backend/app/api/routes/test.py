from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.api.deps import DBDep, auth0
from app.schemas.example import ExampleRequest, ExampleResponse

router = APIRouter(prefix="/test", tags=["Test"])


@router.post("/", response_model=ExampleResponse)
async def example_endpoint(
    db: DBDep,
    example_request_data: ExampleRequest,
    claims: dict = Depends(auth0.require_auth()),
):
    """
    A test endpoint to demonstrate Auth0 integration.
    This will be written in the OpenAPI schema as a GET request to /test/
    with a response model of ExampleResponse.
    """

    # Your logic here
    print(claims)  # Example usage of claims
    print(example_request_data)

    # test the session dependency
    await db.execute(text("SELECT 1"))

    return {"message": "Hello from your endpoint!", "claims": claims}
