import click

from core import Solver, Languages
from core.language import Status
from core.exceptions import InvalidWordLengthError, WordNotFoundError, InvalidAnswerError
from core.validations import validate_word, validate_answer


@click.group()
def main():
    pass


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
@click.option("--verbose", is_flag=True, help="Show top 10 possible words.")
def suggest(lang: str, step: tuple, verbose: bool):
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

    click.echo(f"suggestion: {solver.best_guess()}")
    click.echo(f"remaining: {total}")

    if verbose:
        click.echo("\ntop possible words:")
        for entry in solver.possible_words():
            click.echo(f"  {entry['word']}")
