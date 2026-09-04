# DATABASE.md

MongoDB Atlas. Status: **not yet implemented** — schema below is the plan for
Phase 5+, to be refined as access patterns become concrete.

## Collections (MVP)

### users
```
_id, email (unique, indexed), password_hash, display_name, profile_image_url,
created_at, updated_at
```

### clothing_items
```
_id, user_id (indexed), image_url, category, subcategory, colors[], pattern,
material, style[], formality, season[], gender_category, ai_analyzed (bool),
created_at, updated_at
```
Index: `{user_id: 1, category: 1}`, `{user_id: 1, created_at: -1}`

### outfits
```
_id, user_id (indexed), name, item_ids[] (refs clothing_items),
generated_by ("manual" | "ai"), created_at, updated_at
```

### posts
```
_id, user_id (indexed), outfit_id (ref), image_url, caption, tags[],
like_count, save_count, created_at
```
Index: `{created_at: -1}` for feed pagination (cursor on `_id`/`created_at`)

### likes
```
_id, user_id, post_id, created_at
```
Unique compound index: `{user_id: 1, post_id: 1}`

### saved_posts
```
_id, user_id, post_id, created_at
```
Unique compound index: `{user_id: 1, post_id: 1}`

### follows
```
_id, follower_id, following_id, created_at
```
Unique compound index: `{follower_id: 1, following_id: 1}`

### brands
```
_id, name, logo_url, description, website, social_links{}, categories[]
```

### products
```
_id, brand_id (indexed), name, image_url, price, currency, category, colors[],
sizes[], product_url, availability, tags[], created_at
```
Index: `{category: 1, colors: 1}`, text index on `{name, tags}` for search

## Ownership Rule

Every query against `clothing_items`, `outfits`, `posts` (for mutation),
`likes`, `saved_posts` filters by `user_id` matching the authenticated user
at the repository layer — never trust an ID from the client alone.

## Deletion / Privacy

Account deletion (`DELETE /users/me`) must cascade or soft-delete:
clothing_items, outfits, posts, likes, saves, follows tied to that user_id.
Exact cascade strategy to be finalized in Phase 6 (auth) alongside privacy
requirements (Section 58 of the master spec).