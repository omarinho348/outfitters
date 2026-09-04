# API.md

Base URL (dev): `http://<LAN-IP>:8000/api/v1`

All routes versioned under `/api/v1`. Auth via `Authorization: Bearer <access_token>`
unless noted public.

Status: **not yet implemented.** This file will be filled in as each router ships,
per phase. Structure below is the planned surface, not a guarantee of final shape.

## Planned Routes

### `/api/v1/auth` (public)
- `POST /register` — email, password → user + tokens
- `POST /login` — email, password → tokens
- `POST /refresh` — refresh token → new access token
- `POST /logout` — invalidate refresh token

### `/api/v1/users` (auth required)
- `GET /me` — current user profile
- `PATCH /me` — update profile
- `DELETE /me` — account deletion (required for store compliance)

### `/api/v1/clothing` (auth required, ownership enforced)
- `POST /` — create clothing item (with image)
- `GET /` — list own clothing (paginated, filterable)
- `GET /{id}` — get one (must belong to user)
- `PATCH /{id}` — edit metadata
- `DELETE /{id}`

### `/api/v1/outfits` (auth required)
- `POST /` — create outfit (manual or AI-saved)
- `GET /` — list own outfits
- `GET /{id}`
- `PATCH /{id}`
- `DELETE /{id}`

### `/api/v1/ai`
- `POST /analyze-clothing` — image → structured metadata (rate-limited)
- `POST /generate-outfit` — NL or structured request → recommendations (rate-limited)
- `POST /complete-outfit` — outfit → missing piece + product matches (rate-limited)

### `/api/v1/posts` (social feed)
- `POST /` — create post from an outfit
- `GET /feed` — cursor-paginated feed
- `GET /{id}`
- `DELETE /{id}`
- `POST /{id}/like`, `DELETE /{id}/like`
- `POST /{id}/save`, `DELETE /{id}/save`

### `/api/v1/social`
- `POST /follow/{user_id}`, `DELETE /follow/{user_id}`
- `GET /users/{id}/followers`, `GET /users/{id}/following`

### `/api/v1/brands` (public read)
- `GET /` — list brands
- `GET /{id}`

### `/api/v1/products` (public read)
- `GET /` — search/filter (category, color, price range, brand)
- `GET /{id}`

## Conventions

- Consistent error shape: `{"detail": "message"}` with correct HTTP status codes.
- Cursor pagination: `?cursor=<id>&limit=20` → `{"items": [...], "next_cursor": ...}`
- No internal DB fields (e.g. Mongo `_id` raw ObjectId) leak into responses —
  serialize to `id: str`.