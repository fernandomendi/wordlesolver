# Tests module (`tests/`)

## Responsibility

Holds automated tests for CLI, API, and core logic.

## Current structure

Tests are organized in dedicated files by domain (API, CLI, parsing, validations, filtering, theory).

## Running tests

```bash
uv sync --extra dev
uv run pytest tests/ -m "not slow"
```

## How to add tests

1. Place tests in the most relevant module file.
2. Prefer focused, behavior-based tests over implementation details.
3. Add parametrized cases where inputs vary.
4. Mark expensive tests with `@pytest.mark.slow`.
5. Keep assertions on observable contracts (return shape, errors, statuses).

## Style notes

- Do not document every individual test in markdown.
- Keep intent clear through test names and compact assertions.
