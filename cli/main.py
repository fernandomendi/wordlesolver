import click

from core import parse_language, parse_steps


@click.command()
@click.option(
    "--lang",
    required=True,
    type=str,
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
    try:
        language = parse_language(lang)
    except ValueError as error:
        raise click.BadParameter(str(error), param_hint="--lang") from error

    try:
        steps = parse_steps(step)
    except ValueError as error:
        raise click.BadParameter(str(error), param_hint="--step") from error

    if tui:
        from cli.tui import run
        run(language, steps)
    else:
        from cli.command import run
        run(language, steps, verbose)
