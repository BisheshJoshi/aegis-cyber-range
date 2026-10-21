# Contributing to AEGIS

This is a final-year academic project; contributions are primarily by the author.
These notes keep the codebase consistent.

## Golden rule
**Only ever target the bundled lab container (`localhost`).** Never add code paths,
defaults, or examples that point tooling at systems you do not own. See the legal
notice in the root `README.md` (UK Computer Misuse Act 1990).

## Dev setup
- Python 3.10+ for `attacker/` and `defender/` (each has its own `requirements.txt`).
- Docker + Docker Compose for the lab target (`docker/`).
- Keep secrets in `.env` (never commit; `.env.example` documents the keys).

## Conventions
- Small, documented modules; current modules are **stubs** marked with `# SCAFFOLD`.
- Both attacker and defender emit events using the shared contract in `events/SCHEMA.md`.
- Prefer standard library + the pinned deps; keep the stack £0.

## Commits
- Conventional-ish messages (`feat:`, `fix:`, `docs:`, `chore:`).
- Work on `main` for now; feature branches once the scaffold stabilises.
