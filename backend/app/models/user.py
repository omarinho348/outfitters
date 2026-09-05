from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserInDB(BaseModel):
    id: str
    email: EmailStr
    password_hash: str
    display_name: str
    profile_image_url: str | None = None
    created_at: datetime
    updated_at: datetime
