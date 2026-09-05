from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import get_db
from app.routers import auth, users

app = FastAPI(title="Outfitters API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


@app.on_event("startup")
async def on_startup():
    db = get_db()
    await db.users.create_index("email", unique=True)


@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.ENVIRONMENT}
