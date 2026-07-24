# Wordle Solver — Agent Instructions

## General

See [`../AGENTS.md`](../AGENTS.md) for cross-repo conventions (GitHub CLI alias, git identity, Python venv).

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
