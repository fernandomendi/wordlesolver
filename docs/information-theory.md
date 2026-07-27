# Information theory behind the solver

This solver chooses guesses using Information Theory.

## Intuition

A good guess is one that, on average, gives feedback patterns that split the
remaining candidates as much as possible.

If one guess tends to produce many distinct feedback outcomes (and balanced
outcomes), it gives more information and reduces uncertainty faster.

## Entropy (brief)

For one candidate guess `g`, against current possible secrets `S`:

1. Simulate Wordle feedback for each `s in S`.
2. Count how often each feedback pattern appears.
3. Convert counts to probabilities `p_i`.
4. Compute entropy:

`H(g) = - Σ p_i * log2(p_i)`

Higher entropy means the guess is expected to be more informative.

In code this is implemented in `core/theory.py`:
- `entropy(word, possible_words)`
- `compute_entropies(all_words, possible_words, ...)`

## From one word to best suggestions

The solver computes entropy for each allowed guess word, then combines:

- **entropy signal** (exploration power)
- **word prior probability** from the language word list
- **is_possible boost** for words still in the candidate set

This blend forms a `guessability` score in `core/solver.py` (`_ranked()`), then:

- `best_guess()` returns top-ranked word
- `suggestions()` returns top 10 by guessability
- `possible_words()` returns top 10 currently feasible secrets

### Word prior probability

The word list is stored as plain `words.txt` in ranked line order. The higher
the line rank, the higher the prior probability.

In `core/data_tools.py`, lines are validated, normalized, assigned `id=1..N`,
and then mapped through a sigmoid curve:

```python
x_vals = np.linspace(-10, 10, total_words)
words["probability"] = words["id"].apply(lambda x: sigmoid(x_vals[total_words - x]))
```

That makes top-ranked words start near `1.0` and lower-ranked words taper
smoothly toward `0.0`.

## Why this works in practice

- Early turns: entropy helps eliminate many possibilities quickly.
- Late turns: probability + possible-word boost favors finishing with real
  candidate words.
- Incremental filtering after each step keeps search space focused.

## Notes

- Entropy is recomputed on the current filtered set, not fixed globally.
- Results are cached to `.cache/` for repeated states.
- This is a heuristic optimizer, not a formal guaranteed-minimum-turn proof.
