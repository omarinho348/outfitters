# AI.md

## Principle

AI is used in exactly three places. Everywhere else is normal code.

1. **Clothing image analysis** — image → structured metadata
2. **Outfit generation/reasoning** — reranking rule-based candidates
3. **Natural-language parsing** — NL request → structured filters (styling
   requests and shop search)

## Models

- Vision analysis: `gpt-4o-mini` (or current cheapest capable vision model —
  verify against OpenAI's current pricing/model list before implementation,
  since this may have changed since training data cutoff).
- Reasoning/reranking: same tier, text-only, small context (structured
  wardrobe data only, never raw images re-sent).
- NL parsing: same tier, structured output mode.

Model choice will be re-verified against current OpenAI docs at implementation
time (Phase 8), not assumed from training data.

## Cost Control Rules

- Analyze each clothing item once at upload time. Store result. Never
  re-analyze on every outfit request.
- Never send the full wardrobe as images to the API for a styling request —
  only stored structured metadata (text) goes to the LLM.
- Outfit generation pipeline does the heavy lifting with rule-based filtering
  and scoring (color/style/season/formality compatibility); AI only reranks
  a short candidate list (~5-10), not the entire wardrobe.
- Shop search: normal DB query does the retrieval; AI only converts NL query
  → structured filter object. AI never inspects the product catalog directly.
- All AI endpoints: authenticated, rate-limited per-user (daily cap TBD in
  Phase 8 based on observed cost), request/response logged with token counts.

## Structured Output Schema (clothing analysis) — draft

```json
{
  "category": "pants",
  "subcategory": "jeans",
  "colors": ["black"],
  "pattern": "solid",
  "material": "denim",
  "style": ["casual", "streetwear"],
  "formality": "casual",
  "season": ["fall", "winter", "spring"],
  "gender_category": "unisex"
}
```

Validated server-side with a Pydantic model before insertion. Invalid/missing
fields default to `null`/empty and are flagged for user correction — never
silently dropped or guessed further.

## Tracking (from day one)

Log per AI call: user_id, endpoint, model, input tokens, output tokens,
latency_ms, success/failure, timestamp. Stored in a `ai_usage_logs` collection.
Used to build real cost dashboards before public launch, not guessed at.

## Status

Not yet implemented. Prompts, exact schemas, and rate limits will be finalized
and tested in Phase 8 (clothing analysis) and Phase 10 (outfit generation).