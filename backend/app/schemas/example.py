from typing import Annotated

from pydantic import BaseModel, Field


class ExampleResponse(BaseModel):
    message: str = Field(description="The response message")
    claims: dict = Field(description="The claims associated with the response")

    # test integer with response validation (needs to be bigger than 0 and not null)
    test_value: Annotated[int, Field(gt=0)] | None = Field(
        default=None, description="A test integer value"
    )


class ExampleRequest(BaseModel):
    name: str = Field(description="The name to be processed")
    age: Annotated[int, Field(ge=0)] | None = Field(
        default=None, description="The age of the person, must be non-negative"
    )

    class Config:
        json_schema_extra = {"example": {"name": "John Doe", "age": 30}}
