# Interaction spec (shared Web + TUI contract)

Defines canonical game interaction behavior. Web frontend and future TUI should follow same rules, even if presentation differs.

## Grid model

- 6 attempts (rows)
- 5 letters per attempt (columns)
- Only active row is editable
- Submitted rows are locked

## Letter input

- Accept `A-Z` only for now
- Store/display uppercase in grid; normalize to lowercase when building API payload
- Typing writes focused cell and moves focus right by one cell
- At column 5, typing does not wrap; focus stays on column 5

## Feedback state model

Each cell has one of 4 UI states:

1. `unset` (white)
2. `correct` (green)
3. `misplaced` (yellow)
4. `absent` (gray)

`unset` is not valid for submission.

Cycle order is fixed:

- `unset -> correct -> misplaced -> absent -> unset`

## Keyboard controls

- `ArrowLeft` / `ArrowRight`: move focus within active row
- `ArrowUp` / `ArrowDown`: ignored
- `Space`: cycle feedback state on focused cell
- `Backspace`: clear current cell; if current cell empty, move left then clear
- `Enter`: attempt to submit active row

## Mouse controls

- Click cell: focus cell
- Click focused/unfocused cell: cycle feedback state

## Submit behavior (`Enter`)

- Validate active row before submit:
  - exactly 5 letters
  - all 5 feedback states set (no `unset`)
- If invalid:
  - block submit
  - keep focus on active row
  - show inline validation hint
- If valid:
  - convert feedback to API answer string using mapping:
    - `correct -> "0"`
    - `misplaced -> "1"`
    - `absent -> "2"`
  - submit step using full `steps` history payload
  - lock current row
  - move active cursor to next row
- After row 6 submit:
  - lock grid
  - disable editing
  - show terminal state with `Reset game` action

## Language behavior

- Supported: `en`, `es`
- If user changes language with existing progress:
  - show confirmation prompt
  - on confirm: reset draft row, history, results, and errors
  - on cancel: keep current state

## API coupling rules

Request contract for each step:

```json
{ "guess": "tares", "answer": "12221" }
```

Full payload:

```json
{
  "language": "en",
  "steps": [
    { "guess": "tares", "answer": "12221" }
  ]
}
```

## Error UX contract

- On API 400/validation errors:
  - show dismissible top error banner with backend message
  - show red visual cue on entire active row
  - preserve current input/history so user can correct and retry

## Result surface scope (for #48)

- Minimum success panel must show:
  - `best_guess`
  - `total_possible`
- Place panel below grid.
- Detailed ranking lists (`possible_words`, `suggestions`) are deferred to #47.

## Accessibility baseline (required)

- Visible focus ring on active cell
- Full keyboard-only flow for edit + cycle + submit + dismiss error
- `aria-label` per cell including row/column and current status
- Error banner dismiss button reachable and actionable via keyboard

## Out of scope for this spec

- Ranking panels details (`possible_words`, `suggestions`) UI layout
- Animations and advanced theming
- Accessibility refinements beyond baseline requirements above
