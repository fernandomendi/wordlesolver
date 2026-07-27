# Core module (`core/`)

## Responsibility

Implements Wordle solving logic shared by all interfaces.

Main parts:
- `solver.py`: stateful `Solver`
- `filter.py`: candidate filtering by feedback
- `theory.py`: entropy computation
- `cache.py`: entropy cache read/write
- `parsing.py`: shared input parsing
- `validations.py`: input/data validations
- `models.py`: shared classes (`Language`, `Step`, etc.)
- `feedback.py`: Wordle feedback computation

## Public usage

Typical flow:

1. Create `Solver(language)`
2. Add one or more steps (`guess`, `answer`)
3. Read outputs:
   - `best_guess()`
   - `possible_words()`
   - `suggestions()`
   - `total_possible()`

## Notes

- Word data is loaded from package resources (`core/data/...`), not direct filesystem paths.
- `.cache/` can be deleted safely; values are recomputed when needed.
- Math overview is documented in [`docs/information-theory.md`](../docs/information-theory.md).
