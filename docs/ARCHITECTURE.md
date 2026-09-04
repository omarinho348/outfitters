# ARCHITECTURE.md

## Overview

```
React Native App (Expo + TS)
        │  HTTPS
        ▼
FastAPI Backend (monolith)
        │
   ┌────┼────────────┬───────────────┐
   ▼    ▼             ▼               ▼
MongoDB Atlas   Cloudinary       OpenAI API
(users, closet, (images: clothing, (vision analysis,
outfits, posts,  outfit, profile,   outfit reasoning,
brands, products) product photos)   NL query parsing)
```

No microservices, no message queue, no Kubernetes. A well-structured monolith,
built to evolve — not to impress.

## Backend Layers

```
app/
  main.py         # FastAPI app, middleware, router mounting
  config.py       # env-based settings (pydantic-settings)
  database.py     # Mongo connection/client
  models/         # Pydantic models representing DB documents
  schemas/        # Request/response schemas (may differ from models)
  routers/        # Thin route handlers — no business logic
  services/       # Business logic (outfit generation, AI orchestration, etc.)
  repositories/   # DB access layer — every query enforces ownership here
  auth/           # JWT issuance/verification, password hashing, dependencies
  ai/             # OpenAI client wrapper, prompt templates, schema validation
  storage/        # Cloudinary upload/delete wrapper
  utils/
  tests/
```

Rule: routers call services, services call repositories. Routers never touch the
database directly. Repositories never contain business logic.

## Mobile Layers

Starts flat, moves to feature-based once features multiply:

```
src/
  app/            # Expo Router file-based routes
  components/     # Shared/reusable UI components
  features/       # auth/, closet/, outfits/, shop/, social/, ai/
  services/       # API client, typed fetch wrappers
  hooks/
  store/          # Global state (auth token, user)
  types/
  constants/
  utils/
```

## Data Flow: AI Clothing Analysis

```
Camera/Gallery → client resize/compress → upload to backend
  → backend uploads to Cloudinary → backend calls OpenAI vision
  → structured JSON validated with Pydantic
  → returned to client for user confirmation/edit
  → confirmed metadata saved to MongoDB (never blind-inserted)
```

## Data Flow: AI Outfit Generation

```
User request (NL or structured filters)
  → backend interprets request (lightweight parse, AI only if NL)
  → retrieve user's structured wardrobe metadata from MongoDB (never re-send images)
  → filter candidates programmatically
  → generate combinations (rule-based)
  → score compatibility (rule-based: color/style/season/formality)
  → AI reranking/reasoning on top-N candidates only
  → return recommendations
```

## Data Flow: AI Outfit Completion → Shop

```
User's selected outfit items → AI identifies missing category + attributes
  → structured requirement (e.g. {category: "jacket", color: "black", style: "oversized"})
  → normal MongoDB query against Product catalog (no AI touches product data directly)
  → return matching products from local brands
```

## Environments

Development / Staging / Production — separate `.env` files, separate Mongo
databases (or Atlas clusters), never share secrets across environments.

## Security Boundaries

- Mobile app never holds: OpenAI key, Mongo credentials, Cloudinary secret.
- Backend is the only component with credentials to external services.
- Every backend endpoint that reads/writes user-owned data enforces
  `resource.user_id == current_user.id` at the repository layer.