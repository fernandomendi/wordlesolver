# Frontend module (`frontend/`)

## Current status

Frontend is scaffold-level at the moment (Dockerfile only).

## Planned role

- Provide web UI for entering guesses and feedback.
- Call API `POST /solve`.
- Display:
  - best guess
  - remaining possible words
  - top suggestions
  - remaining count

## Next implementation steps

1. Scaffold React app.
2. Build input + feedback form.
3. Render solver outputs.
4. Wire to Flask API.
