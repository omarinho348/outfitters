# AGENTS.md — Rules for AI Coding Agents

This file governs how any AI agent (Claude, or another model) works on this repository.
Read this file, then `docs/STATUS.md`, before making any change.

## Core Rules

1. **The repo is the source of truth**, not conversation history. Never assume context
   from a previous chat that isn't reflected in `docs/`.
2. **Do not silently change**: framework, database, auth approach, storage provider,
   AI provider, or overall architecture. If a change seems warranted, write it up in
   `docs/DECISIONS.md` as a proposal and flag it to the human before implementing.
3. **MVP scope is fixed** (see `docs/STATUS.md` → Current MVP Scope). Do not add
   features outside it without the human explicitly approving scope expansion.
4. **No AI where normal code works.** AI is only for: clothing image analysis, outfit
   generation/reasoning, and natural-language → structured query parsing. Everything
   else (feed, likes, follows, search filtering, CRUD) is normal backend logic.
5. **Backend is the authority.** Every mutating or reading endpoint must enforce
   resource ownership server-side. Never trust the client.
6. **Never commit secrets.** `.env` is gitignored; only `.env.example` with placeholders
   is committed.
7. **Never claim something works without testing it.** If a command failed, say so.
   If an endpoint wasn't tested, say so.

## Workflow for Every Significant Task

1. **Read** — relevant docs + existing code.
2. **Plan** — state what will change, which files, why, and risks. Get confirmation
   for anything touching auth, data model, or cost-bearing AI calls.
3. **Implement** — focused changes only.
4. **Test** — run whatever tests/checks apply. State results honestly.
5. **Review** — check for bugs, security issues, ownership bugs, duplication.
6. **Document** — update the relevant file(s) in `docs/`.
7. **Commit** — small, meaningful commit message (`feat:`, `fix:`, `docs:`, `chore:`).
8. **Report** — what changed, what was tested, what remains, next step.

## Session Handoff

At the end of every session, update `docs/STATUS.md` with:
- Completed
- Files changed
- Tests run
- Known issues
- Decisions made
- Current state
- Next task

A new session must be able to pick up work using only the repo contents.