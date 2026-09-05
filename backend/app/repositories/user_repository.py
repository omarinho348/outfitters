from datetime import datetime, timezone

from bson import ObjectId

from app.database import get_db


def _serialize(doc: dict) -> dict:
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return doc


async def get_by_email(email: str) -> dict | None:
    db = get_db()
    doc = await db.users.find_one({"email": email})
    return _serialize(doc) if doc else None


async def get_by_id(user_id: str) -> dict | None:
    db = get_db()
    try:
        object_id = ObjectId(user_id)
    except Exception:
        return None
    doc = await db.users.find_one({"_id": object_id})
    return _serialize(doc) if doc else None


async def create_user(email: str, password_hash: str, display_name: str) -> dict:
    db = get_db()
    now = datetime.now(timezone.utc)
    result = await db.users.insert_one(
        {
            "email": email,
            "password_hash": password_hash,
            "display_name": display_name,
            "profile_image_url": None,
            "created_at": now,
            "updated_at": now,
        }
    )
    doc = await db.users.find_one({"_id": result.inserted_id})
    return _serialize(doc)
