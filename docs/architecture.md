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

## Frontend + API architecture (current)

### Runtime roles

- `api` (Flask): backend API service on `http://localhost:5000`
- `frontend` (React): UI code in `frontend/src/`
- `vite`: frontend development/build toolchain
  - local dev server on `http://localhost:5173`
  - production build output in `frontend/dist/`

### Local development request flow

1. Browser opens frontend at `http://localhost:5173` (`npm run dev`).
2. Frontend calls `/api/*` paths.
3. Vite proxy forwards `/api/*` to Flask (`http://localhost:5000/*`).

This keeps frontend code using relative API paths and avoids direct browser cross-origin calls during local development.

### Docker Compose request flow

When both services run in Docker/Podman, browser still opens `http://localhost:5173`, but service-to-service networking changes:

1. Frontend container runs Vite on `5173`.
2. API container runs Flask on `5000`.
3. Vite proxy target is set to `http://api:5000` (Docker service DNS name), not `localhost:5000`.

Inside containers, `localhost` points to the same container itself; service names are required for cross-container calls.

**Supported container runtimes:** Docker (via `docker compose`) and Podman (via `podman-compose`). Both use `Containerfile`/`podman-compose.yml` naming conventions.

### Production shape

- `npm run build` generates static frontend assets in `frontend/dist/`.
- Static assets are served by a web/static host.
- Flask remains a separate API service.
- Frontend should keep `/api/*` contract, with routing/proxy handled by deployment ingress/reverse proxy.
