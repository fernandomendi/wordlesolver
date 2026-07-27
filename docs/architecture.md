# Architecture

## Overview

The project is split into one shared solver core and multiple interfaces:

- `core`: domain logic and scoring
- `cli`: local command interface
- `api`: HTTP interface for frontend/external clients
- `frontend`: UI layer (in progress)

## Data flow

1. Input is provided as `(language, steps)`.
2. Input is parsed/validated (`core/parsing.py`, `core/validations.py`).
3. `Solver` applies steps incrementally to narrow candidate words.
4. `Solver` computes/loads entropy stats and ranking metrics.
5. Interface returns:
   - `best_guess`
   - `possible_words`
   - `suggestions`
   - `total_possible`

## Core design decisions

- `Solver` owns state (`_steps`, `_possible`, `_entropies`).
- Word lists are packaged in `core/data/` and loaded via `importlib.resources`.
- Entropy cache is file-based in `.cache/` and safe to regenerate.
- API rejects impossible solver states (`total_possible == 0`) with HTTP 400.

## Interface separation

- CLI and API both reuse shared parser helpers from `core/parsing.py`.
- CLI maps validation errors to `click.BadParameter`.
- API maps validation errors to `BadRequest` JSON responses.
