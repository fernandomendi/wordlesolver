import click

from core import Solver, Languages
from core.language import Status
from core.exceptions import InvalidWordLengthError, WordNotFoundError, InvalidAnswerError
from core.validations import validate_word, validate_answer


@click.group()
def main():
    pass


# TODO: implement `interactive` command (issue #39) using Textual TUI.
# Design:
#   uv run wordlesolver interactive --lang es
#   uv run wordlesolver interactive --lang es --step careo 12110  (preload game state)
#
# - Fixed terminal layout: grid of guesses, live suggestion, remaining word count
# - Consumes core/ directly (no API hop)
# - --step flags preload steps before the TUI opens (same pattern as `suggest`)
# - Deferred until after React frontend — Textual borrows from React concepts


@main.command()
@click.option(
    "--lang",
    default="en",
    show_default=True,
    type=click.Choice(["en", "es"]),
    help="Language of the Wordle game."
)
@click.option(
    "--step",
    type=(str, str),
    multiple=True,
    metavar="GUESS ANSWER",
    help="A guess and its feedback (repeatable). Example: --step careo 12110"
)
@click.option("--count", is_flag=True, help="Show number of remaining possible words.")
@click.option("--top", default=0, help="Show top N possible words.")
def suggest(lang: str, step: tuple, count: bool, top: int):
    """Return the next best guess given accumulated steps."""
    match lang:
        case "en":
            language = Languages.EN
        case "es":
            language = Languages.ES

    solver = Solver(language)

    for guess, answer in step:
        try:
            validate_word(guess, language)
        except (InvalidWordLengthError, WordNotFoundError) as e:
            raise click.BadParameter(str(e), param_hint="--step GUESS")
        try:
            validate_answer(answer)
        except InvalidAnswerError as e:
            raise click.BadParameter(str(e), param_hint="--step ANSWER")
        solver.add_step(guess, answer)

    total = solver.total_possible()

    if total == 0:
        raise click.ClickException("No possible words remaining. Check your feedback.")

    if total == 1:
        word = solver.possible_words()[0]["word"]
        click.echo(f"answer: {word}")
        return

    click.echo(solver.best_guess())

    if count:
        click.echo(f"remaining: {total}")

    if top:
        for entry in solver.possible_words()[:top]:
            click.echo(f"  {entry['word']}")
