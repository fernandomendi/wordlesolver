# CLI module (`cli/`)

## Responsibility

Provides the command-line interface on top of `core`.

Files:
- `main.py`: click entrypoint/options parsing
- `command.py`: command-mode execution logic
- `tui.py`: placeholder for future TUI mode

## Usage

```bash
uv run wordlesolver --lang en
uv run wordlesolver --lang en --step tares 12221 --step moust 12211
uv run wordlesolver --lang es --step careo 12110 -v
```

## Behavior

- Parses language and steps via `core.parsing`.
- Converts core validation errors into CLI-friendly parameter errors.
- `--verbose` prints words left and top candidates.
