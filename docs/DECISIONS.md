# DECISIONS.md

Record of architecture/product decisions. Newest first. Never delete history —
if a decision is reversed, add a new entry noting the reversal and why.

---

## 2026-09-05 — Initial technical decisions (Session 1)

**Decision:** Confirmed stack — React Native/Expo/TS + Expo Router, FastAPI +
Python 3.12 + uv, MongoDB Atlas M0, Cloudinary for images, OpenAI gpt-4o-mini
class models, JWT auth (access+refresh) with bcrypt password hashing.

**Why:** Matches the human's existing skill set (Python/FastAPI/Mongo), all
free-tier-capable, no vendor lock-in that isn't easily migrated (Cloudinary
and S3-compatible storage are swappable later).

**Alternatives considered:** Cloudflare R2 for images (rejected for MVP —
Cloudinary's built-in resizing/thumbnailing saves backend work; revisit if
Cloudinary cost becomes material at scale).

---

## 2026-09-05 — Comments cut from MVP

**Decision:** Social feed ships with like/save/follow but not comments.

**Why:** Target demographic includes teenagers. Comments require a moderation
pipeline (report/block/remove) to be safe at public launch. Shipping comments
without that pipeline is a safety liability, not just a feature gap. Comments
will ship in the same phase as report/block tooling (pre-public-launch
hardening), not in the private-testing MVP.

**Status:** Approved by stakeholder.

---

## 2026-09-05 — Sequencing: Manual Outfit Builder before AI Stylist

**Decision:** Build Phase 9 (manual builder) before Phase 8 (AI clothing
analysis) is completed end-to-end... clarification: AI *clothing analysis*
(Phase 8) still comes before the manual builder needs it, but AI *outfit
generation* (Phase 10) comes after the manual builder (Phase 9). Manual
builder does not depend on AI stylist and gives a testable, demoable feature
sooner.

**Why:** De-risks the roadmap — a working manual flow exists even if AI
generation takes longer than expected to tune.

---

## Template for New Entries

```
## YYYY-MM-DD — <short title>

**Decision:** what was decided
**Why:** reasoning
**Alternatives considered:** what else was evaluated and why rejected
**Status:** proposed / approved / reversed
```