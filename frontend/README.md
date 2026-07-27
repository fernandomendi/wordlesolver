# Frontend module (`frontend/`)

## Responsibility

Provides React web client for Wordle solver flow and API integration.

## Stack

- React + Vite
- Tailwind CSS
- Oxlint (frontend lint command from Vite template)

## Current scaffold

- Vite React app bootstrap
- Tailwind enabled through `@tailwindcss/vite`
- API proxy in `vite.config.js`:
  - `/api/*` → `http://localhost:5000/*`
- Base folders:
  - `src/components/`
  - `src/hooks/`
  - `src/api/`

## Run locally

```bash
cd frontend
npm install
npm run dev
```

## Planned next steps

1. Guess + feedback input UI.
2. Solver submission flow using `src/api/client.js`.
3. Results panels (best guess, remaining words, suggestions).
