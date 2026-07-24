import click

from core import Solver, Languages
from core.exceptions import InvalidWordLengthError, WordNotFoundError, InvalidAnswerError
from core.validations import validate_word, validate_answer


def _dim(text: str) -> str:
    return click.style(f"  {text}", fg="bright_black")


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
@click.option("--top-probable", "top_probable", default=0, help="Show top N most probable answers.")
@click.option("--top-suggestions", "top_suggestions", default=0, help="Show top N best next guesses by entropy.")
def suggest(lang: str, step: tuple, count: bool, top_probable: int, top_suggestions: int):
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
        click.echo(click.style(solver.possible_words()[0]["word"], bold=True))
        return

    if count:
        click.echo(_dim(f"remaining: {total}"))

    if top_probable:
        click.echo(_dim("top probable:"))
        for entry in solver.possible_words()[:top_probable]:
            click.echo(_dim(f"  {entry['word']}"))

    if top_suggestions:
        click.echo(_dim("top suggestions:"))
        for entry in solver.suggestions()[:top_suggestions]:
            click.echo(_dim(f"  {entry['word']}"))

    click.echo(click.style(solver.best_guess(), bold=True))
