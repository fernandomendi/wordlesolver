import click

from core import Languages
from core.models import Language
from core.validations import validate_word, validate_answer


def _parse_steps(step: tuple, language: Language) -> list[tuple[str, str]]:
    steps = []
    for guess, answer in step:
        try:
            validate_word(guess, language)
        except ValueError as e:
            raise click.BadParameter(str(e), param_hint="--step GUESS")
        try:
            validate_answer(answer)
        except ValueError as e:
            raise click.BadParameter(str(e), param_hint="--step ANSWER")
        steps.append((guess, answer))
    return steps


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
@click.option("--tui", is_flag=True, help="Launch interactive Textual TUI.")
@click.option("--verbose", "-v", is_flag=True, help="Show words left, top probable, and top suggestions.")
def main(lang: str, step: tuple, tui: bool, verbose: bool):
    """Wordle solver — returns the next best guess given accumulated steps."""
    match lang:
        case "en":
            language = Languages.EN
        case "es":
            language = Languages.ES

    steps = _parse_steps(step, language)

    if tui:
        from cli.tui import run
        run(language, steps)
    else:
        from cli.command import run
        run(language, steps, verbose)
