# Development workflow

## Tooling

- Package/runtime manager: `uv`
- Test framework: `pytest`
- CI: GitHub Actions

## Common commands

Install deps:

```bash
uv sync --extra test
```

Run tests:

```bash
uv run --extra test pytest tests/ -m "not slow"
```

Run CLI:

```bash
uv run wordlesolver --lang en
```

Run API:

```bash
uv run flask --app api run --host 0.0.0.0 --port 5000
```

## CI checks

Current CI validates:

1. Python tests (`.github/workflows/unit_tests.yml`)
2. Markdown lint + link checks (`.github/workflows/docs_checks.yml`)

## Branch and PR conventions

- One branch per issue (`feature/<issue-number>-<short-description>`)
- Squash merge into `main`
- One PR per issue unless explicitly grouped

## Documentation update expectations

- Update root `README.md` when setup or top-level usage changes.
- Update module README when module behavior/contracts change.
- Update `docs/` guides when architecture or development workflow changes.
- Keep code comments for non-obvious logic only.
