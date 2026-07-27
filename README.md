# wordlesolver

Wordle solver project with:
- `core` Python solving library
- `cli` command-line interface
- `api` Flask API
- `frontend` React scaffold (in progress)

## Installation

This repository uses `uv`.

```bash
git clone https://github.com/fernandomendi/wordlesolver.git
cd wordlesolver
uv sync --extra test
```

## Quick usage

### CLI

```bash
uv run wordlesolver --lang en
uv run wordlesolver --lang en --step tares 12221 --step moust 12211
uv run wordlesolver --lang en --step tares 12221 -v
```

### API

Run API:

```bash
uv run flask --app api run --host 0.0.0.0 --port 5000
```

Call API:

```bash
curl -X POST http://localhost:5000/solve \
  -H "Content-Type: application/json" \
  -d '{"language":"en","steps":[{"guess":"tares","answer":"12221"}]}'
```

## Testing

```bash
uv run --extra test pytest tests/ -m "not slow"
```

CI also runs:
- unit tests (`pytest -m "not slow"`)
- markdown lint and markdown link checks

## Repository structure

```text
wordlesolver/
├── core/       # Solver logic, filtering, entropy, validations, models
├── cli/        # Click entrypoint and command mode
├── api/        # Flask app and route modules
├── frontend/   # Frontend scaffold
├── tests/      # Pytest suite
├── docs/       # Canonical project documentation
└── scripts/    # Legacy scripts (not part of current supported flow)
```

## Documentation map

- [`docs/README.md`](docs/README.md): docs index
- [`docs/architecture.md`](docs/architecture.md): architecture and data flow
- [`docs/information-theory.md`](docs/information-theory.md): why entropy-based ranking works
- [`docs/development.md`](docs/development.md): development workflow
- [`core/README.md`](core/README.md): core module guide
- [`cli/README.md`](cli/README.md): CLI module guide
- [`api/README.md`](api/README.md): API module guide
- [`frontend/README.md`](frontend/README.md): frontend status and plan
- [`tests/README.md`](tests/README.md): test structure and conventions

## Scripts status

`scripts/` currently contains legacy utilities based on the old layout/import paths
plus small maintenance scripts like `scripts/add_word.py`. They are kept for now
but are not part of the supported v1 CLI/API workflow.
