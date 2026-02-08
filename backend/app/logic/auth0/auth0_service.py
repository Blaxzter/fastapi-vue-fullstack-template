from typing import Any

import httpx

from app.core.auth import get_management_api_token
from app.core.config import settings
from app.schemas.users import UserProfileUpdate


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
