from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.schemas.auth import UserOut

router = APIRouter()


@router.get("/me", response_model=UserOut)
async def get_me(current_user: dict = Depends(get_current_user)):
    return UserOut(**current_user)
