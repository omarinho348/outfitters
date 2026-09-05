import uuid
from datetime import datetime, timedelta, timezone

from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token_jwt,
    decode_token,
)
from app.config import settings
from app.repositories import user_repository, refresh_token_repository


class AuthError(Exception):
    """Raised for any auth failure that should become a 4xx response."""


async def register(email: str, password: str, display_name: str) -> dict:
    existing = await user_repository.get_by_email(email)
    if existing:
        raise AuthError("An account with this email already exists")
    password_hash = hash_password(password)
    return await user_repository.create_user(email, password_hash, display_name)


async def _issue_tokens(user_id: str) -> dict:
    access_token = create_access_token(user_id)
    jti = str(uuid.uuid4())
    refresh_expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    refresh_token = create_refresh_token_jwt(user_id, jti, refresh_expire)
    await refresh_token_repository.store(user_id, jti, refresh_expire)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


async def login(email: str, password: str) -> tuple[dict, dict]:
    user = await user_repository.get_by_email(email)
    if not user or not verify_password(password, user["password_hash"]):
        raise AuthError("Invalid email or password")
    tokens = await _issue_tokens(user["id"])
    return user, tokens


async def refresh(refresh_token: str) -> dict:
    try:
        payload = decode_token(refresh_token)
    except ValueError as exc:
        raise AuthError("Invalid or expired refresh token") from exc

    if payload.get("type") != "refresh":
        raise AuthError("Invalid token type")

    user_id = payload["sub"]
    jti = payload["jti"]

    if not await refresh_token_repository.is_valid(jti, user_id):
        raise AuthError("Refresh token has been revoked or is invalid")

    await refresh_token_repository.revoke(jti)
    return await _issue_tokens(user_id)


async def logout(refresh_token: str) -> None:
    try:
        payload = decode_token(refresh_token)
    except ValueError:
        return
    if payload.get("type") == "refresh":
        await refresh_token_repository.revoke(payload["jti"])
