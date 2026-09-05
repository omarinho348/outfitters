from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RefreshRequest,
    TokenPair,
    UserOut,
)
from app.services import auth_service
from app.services.auth_service import AuthError

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest):
    try:
        user = await auth_service.register(
            payload.email, payload.password, payload.display_name
        )
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return UserOut(**user)


@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest):
    try:
        _, tokens = await auth_service.login(payload.email, payload.password)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    return TokenPair(**tokens)


@router.post("/refresh", response_model=TokenPair)
async def refresh_token(payload: RefreshRequest):
    try:
        tokens = await auth_service.refresh(payload.refresh_token)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    return TokenPair(**tokens)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(payload: RefreshRequest):
    await auth_service.logout(payload.refresh_token)
