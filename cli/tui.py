# TODO: implement Textual TUI (issue #39).
# Design:
#   uv run wordlesolver --tui --lang es
#   uv run wordlesolver --tui --lang es --step careo 12110  (preload game state)
#
# - Fixed terminal layout: grid of guesses, live suggestion, words left
# - Consumes core/ directly (no API hop)
# - steps param preloads game state before the TUI opens
# - Deferred until after React frontend — Textual borrows from React concepts

import click

from core.models import Language


def run(language: Language, steps: list[tuple[str, str]]) -> None:
    raise click.ClickException("TUI not yet implemented (issue #39).")
