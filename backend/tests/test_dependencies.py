from fastapi import HTTPException, status
import pytest
import jwt

from app.config import settings
from app.dependencies import (
    get_current_user,
    get_current_active_user,
    get_current_premium_user,
    get_current_admin,
)


@pytest.fixture
def token():
    payload = {"sub": "username"}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@pytest.mark.asyncio
async def test_get_current_user(patch_get_user_by_username, token):
    user = await get_current_user(token)
    assert user.username == "username"


@pytest.mark.asyncio
async def test_get_current_active_user(patch_get_user_by_username, token):
    user = await get_current_active_user(await get_current_user(token))
    assert user.username == "username"
    assert user.is_banned is False


@pytest.mark.asyncio
async def test_get_current_premium_user(patch_get_user_by_username, token):
    with pytest.raises(HTTPException) as exc_info:
        await get_current_premium_user(await get_current_user(token))
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == "Access denied: Premium users only."


@pytest.mark.asyncio
async def test_get_current_admin(patch_get_user_by_username, token):
    with pytest.raises(HTTPException) as exc_info:
        await get_current_admin(
            await get_current_active_user(await get_current_user(token))
        )
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == "Access denied: Admins only."
