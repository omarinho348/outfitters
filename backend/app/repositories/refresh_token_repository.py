from datetime import datetime, timezone

from app.database import get_db


async def store(user_id: str, jti: str, expires_at: datetime) -> None:
    db = get_db()
    await db.refresh_tokens.insert_one(
        {
            "user_id": user_id,
            "jti": jti,
            "expires_at": expires_at,
            "revoked": False,
            "created_at": datetime.now(timezone.utc),
        }
    )


async def is_valid(jti: str, user_id: str) -> bool:
    db = get_db()
    doc = await db.refresh_tokens.find_one(
        {"jti": jti, "user_id": user_id, "revoked": False}
    )
    return doc is not None


async def revoke(jti: str) -> None:
    db = get_db()
    await db.refresh_tokens.update_one({"jti": jti}, {"$set": {"revoked": True}})
