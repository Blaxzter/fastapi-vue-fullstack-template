from pydantic import BaseModel, Field, HttpUrl


class UserProfileUpdate(BaseModel):
    name: str | None = Field(None, max_length=100, description="User's display name")
    nickname: str | None = Field(None, max_length=50, description="User's nickname")
    picture: HttpUrl | None = Field(None, description="URL to user's profile picture")
    bio: str | None = Field(None, max_length=500, description="User's biography")


class UserProfile(BaseModel):
    sub: str
    name: str | None = None
    nickname: str | None = None
    email: str | None = None
    picture: HttpUrl | None = None
    bio: str | None = None
    email_verified: bool | None = None
