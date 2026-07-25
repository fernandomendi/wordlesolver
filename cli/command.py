import click

from core import Solver
from core.language import Language


def _dim(text: str) -> str:
    return click.style(f"  {text}", fg="bright_black")


def run(language: Language, steps: list[tuple[str, str]], verbose: bool) -> None:
    solver = Solver(language)

    for guess, answer in steps:
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
