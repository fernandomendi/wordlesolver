# Wordle Solver — Agent Instructions

## General

See parent AGENTS file for cross-repo conventions (GitHub CLI alias, git identity, Python venv).

## Repo Structure

```
wordlesolver/
├── core/       # Python library — entropy, filtering, Solver class
├── cli/        # click-based CLI (interactive + command modes)
├── api/        # Flask REST API
├── frontend/   # React web app
└── tests/      # pytest test suite
```

## Package Manager

This repo uses `uv`. Do not use `pip` or `requirements.txt`.

```bash
uv run pytest tests/              # run tests
uv run --extra test pytest tests/ # run tests with test deps
uv run wordlesolver               # run CLI
uv add <package>                  # add dependency
```

## Branching

- Branch protection enforces squash merges on `main`.
- Branch naming: `feature/<issue-number>-<short-description>`
- One PR per issue.

## Data Files

Word lists live in `core/data/` and are shipped inside the package via `importlib.resources`. Do not reference them by filesystem path.

## Cache

Entropy cache is written to `.cache/` at repo root (gitignored). It is safe to delete.

## Documentation style and maintenance

- Root `README.md` is onboarding entrypoint: installation, quick usage, high-level structure, and links.
- `docs/` holds canonical deeper guides (architecture, workflow, policies).
- Module READMEs (`core/`, `cli/`, `api/`, `frontend/`, `tests/`) explain responsibilities, contracts, and extension points.
- Keep documentation tiered:
  - `core` / `api` / `tests`: medium detail
  - `cli` / `frontend`: light-to-medium detail
- Keep code comments for non-obvious logic only; avoid narrating straightforward code.
- Avoid per-test prose in markdown; explain test structure/conventions instead.
- Keep `scripts/` treated as legacy unless explicitly modernized.
