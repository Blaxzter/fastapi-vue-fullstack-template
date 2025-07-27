from typing import Any

import httpx
from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import auth0
from app.core.auth import get_management_api_token
from app.core.config import settings
from app.schemas.users import UserProfile, UserProfileUpdate

router = APIRouter(prefix="/users", tags=["users"])


async def update_auth0_user(user_id: str, update_data: UserProfileUpdate) -> bool:
    """Update user profile in Auth0 using Management API."""
    try:
        token = await get_management_api_token()

        # Prepare user update payload
        user_data: dict[str, Any] = {}
        if update_data.name is not None:
            user_data["name"] = update_data.name
        if update_data.nickname is not None:
            user_data["nickname"] = update_data.nickname
        if update_data.picture is not None:
            user_data["picture"] = str(update_data.picture)

        # Add bio to user_metadata
        if update_data.bio is not None:
            user_data["user_metadata"] = {"bio": update_data.bio}

        if not user_data:
            return True

        # Update user via Management API
        url = f"https://{settings.AUTH0_DOMAIN}/api/v2/users/{user_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=user_data, headers=headers)
            return response.status_code == 200

    except Exception as e:
        print(f"Error updating Auth0 user: {e}")
        return False


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    claims: dict = Depends(auth0.require_auth()),
) -> Any:
    """Get current user profile information."""
    return UserProfile(**claims)


@router.patch("/me", response_model=UserProfile)
async def update_user_profile(
    user_update: UserProfileUpdate,
    claims: dict = Depends(auth0.require_auth()),
) -> Any:
    """Update current user profile information using Auth0 Management API."""
    user_id = claims.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID not found")

    # Update user in Auth0 using Management API
    success = await update_auth0_user(user_id, user_update)

    if not success:
        raise HTTPException(
            status_code=500, detail="Failed to update user profile in Auth0"
        )

    # Return updated user data
    updated_user = claims.copy()

    if user_update.name is not None:
        updated_user["name"] = user_update.name
    if user_update.nickname is not None:
        updated_user["nickname"] = user_update.nickname
    if user_update.picture is not None:
        updated_user["picture"] = str(user_update.picture)
    if user_update.bio is not None:
        updated_user["bio"] = user_update.bio

    return UserProfile(**updated_user)


@router.get("/auth0-management-url")
async def get_auth0_management_url(
    _: dict = Depends(auth0.require_auth()),
) -> dict[str, str]:
    """Get the Auth0 management URL for advanced account settings."""
    return {
        "management_url": f"https://{settings.AUTH0_DOMAIN}/login",
        "note": "For email and password changes, please use Auth0's account management",
    }
