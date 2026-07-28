# API module (`api/`)

## Responsibility

Provides HTTP interface for the solver.

Files:
- `app.py`: Flask app factory, CORS, error handlers
- `routes/health.py`: health endpoint
- `routes/solve.py`: solver endpoint

## Endpoints

### `GET /health`

Returns API liveness status.

### `POST /solve`

Request:

```json
{
  "language": "en",
  "steps": [
    { "guess": "tares", "answer": "12221" }
  ]
}
```

Response:

```json
{
  "best_guess": "smith",
  "possible_words": [{ "word": "smith", "probability": 0.123 }],
  "suggestions": [{ "word": "smith", "guessability": 0.987 }],
  "total_possible": 3
}
```

## Error model

- API returns JSON errors (not HTML pages).
- Invalid inputs or impossible states return HTTP 400.

## Local run

```bash
uv run flask --app api run --host 0.0.0.0 --port 5000
```

## Frontend origin and CORS

- Default allowed frontend origin: `http://localhost:5173` (Vite dev server)
- Override via env var when needed:

```bash
FRONTEND_ORIGINS="http://localhost:5173,http://localhost:3000"
```
