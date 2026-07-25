import click

from core import Solver, Languages
from core.exceptions import InvalidWordLengthError, WordNotFoundError, InvalidAnswerError
from core.validations import validate_word, validate_answer


def _dim(text: str) -> str:
    return click.style(f"  {text}", fg="bright_black")


# TODO: implement --ui flag (issue #39) using Textual TUI.
# Design:
#   uv run wordlesolver --ui --lang es
#   uv run wordlesolver --ui --lang es --step careo 12110  (preload game state)
#
# - Fixed terminal layout: grid of guesses, live suggestion, words left
# - Consumes core/ directly (no API hop)
# - --step flags preload steps before the TUI opens
# - Deferred until after React frontend — Textual borrows from React concepts


@click.command()
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
@click.option("--ui", is_flag=True, help="Launch interactive Textual TUI.")
@click.option("--verbose", "-v", is_flag=True, help="Show words left, top probable, and top suggestions.")
def main(lang: str, step: tuple, ui: bool, verbose: bool):
    """Wordle solver — returns the next best guess given accumulated steps."""
    match lang:
        case "en":
            language = Languages.EN
        case "es":
            language = Languages.ES

    if ui:
        raise click.ClickException("TUI not yet implemented (issue #39).")

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
        click.echo(click.style(solver.possible_words()[0]["word"], bold=True))
        return

    if verbose:
        click.echo(_dim(f"words left: {total}"))
        click.echo(_dim("top probable:"))
        for entry in solver.possible_words()[:10]:
            click.echo(_dim(f"  {entry['word']}"))
        click.echo(_dim("top suggestions:"))
        for entry in solver.suggestions()[:10]:
            click.echo(_dim(f"  {entry['word']}"))

    click.echo(click.style(solver.best_guess(), bold=True))
