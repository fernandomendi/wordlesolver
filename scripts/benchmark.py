"""Benchmark solver performance across a sample of secret words."""

from __future__ import annotations

import argparse
import sys
from importlib import resources
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.feedback import feedback
from core.models import Language
from core.parsing import parse_language
from core.solver import Solver


def render_progress(current: int, total: int, width: int = 20) -> str:
    filled = int(width * current / total)
    bar = "#" * filled + "-" * (width - filled)
    return f"[{bar}] {current}/{total}"


def load_words(language: Language) -> pd.DataFrame:
    resource = resources.files("core.data").joinpath(f"{language.code}/words.csv")
    with resource.open("r") as handle:
        return pd.read_csv(handle)


def steps_per_secret(secret: str, language: Language) -> int:
    solver = Solver(language)
    steps = 0

    while solver.total_possible() > 1 and steps < 6:
        guess = solver.best_guess()
        solver.add_step(guess, feedback(secret, guess))
        steps += 1

    if solver.total_possible() == 1:
        guess = solver.possible_words()[0]["word"]
        solver.add_step(guess, feedback(secret, guess))
        steps += 1
        return steps

    return 7


def benchmark(language: Language, sample_size: int, seed: int | None = None) -> None:
    words = load_words(language)
    if sample_size < 1:
        raise ValueError("Sample size must be at least 1.")
    if sample_size > len(words):
        raise ValueError(f"Sample size must be at most {len(words)}.")

    sample = words.sample(n=sample_size, random_state=seed).reset_index(drop=True)
    steps: list[int] = []
    for index, secret in enumerate(sample.word, start=1):
        print(f"\r{render_progress(index, len(sample))}", end="", flush=True)
        steps.append(steps_per_secret(secret, language))
    print()
    sample["steps"] = steps

    summary = (
        sample["steps"]
        .value_counts()
        .sort_index()
        .rename_axis("steps")
        .reset_index(name="count")
    )
    summary["steps"] = summary["steps"].replace(7, "6+")
    summary["probability"] = summary["count"] / len(sample)

    print("Average steps per word")
    print(f"Mean: {sample.steps.mean():.2f}")
    print(summary[["steps", "probability"]].to_string(index=False, formatters={"probability": "{:,.2%}".format}))


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark solver steps over a sample of words.")
    parser.add_argument("language", help="Target language.")
    parser.add_argument(
        "--sample-size",
        type=int,
        default=100,
        help="Number of secret words to sample (default: 100).",
    )
    parser.add_argument("--seed", type=int, default=None, help="Optional random seed for the sample.")
    args = parser.parse_args()

    language = parse_language(args.language)
    benchmark(language, args.sample_size, seed=args.seed)


if __name__ == "__main__":
    main()
