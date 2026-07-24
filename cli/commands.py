import click

from core import Solver, Languages
from core.exceptions import InvalidWordLengthError, WordNotFoundError, InvalidAnswerError
from core.language import Status
from core.validations import validate_word, validate_answer

CORRECT_COLOR = "green"
MISPLACED_COLOR = "yellow"
ABSENT_COLOR = "white"


def _colored_answer(answer: str) -> str:
    colors = {Status.CORRECT: CORRECT_COLOR, Status.MISPLACED: MISPLACED_COLOR, Status.ABSENT: ABSENT_COLOR}
    return "".join(click.style(ch, fg=colors[ch]) for ch in answer)


@click.command()
@click.option(
    "--lang",
    default="en",
    show_default=True,
    type=click.Choice(["en", "es"]),
    help="Language of the Wordle game."
)
def main(lang: str):
    """Interactively solve a Wordle game step by step."""
    match lang:
        case "en":
            language = Languages.EN
        case "es":
            language = Languages.ES
    solver = Solver(language)

    click.echo(f"Starting solver ({lang.upper()}). Type your guesses and enter the feedback.")
    click.echo("Feedback: 0=correct (green), 1=misplaced (yellow), 2=absent (grey)\n")

    while True:
        total = solver.total_possible()

        if total == 0:
            click.echo(click.style("No possible words remaining. Check your feedback.", fg="red"))
            break

        if total == 1:
            word = solver.possible_words()[0]["word"]
            click.echo(click.style(f"The only word left is: {word}", fg="green", bold=True))
            break

        click.echo(f"Suggested guess: {click.style(solver.best_guess(), fg='cyan', bold=True)}")
        click.echo(f"Possible words remaining: {total}")

        guess = None
        while guess is None:
            raw = click.prompt("Your guess").strip().lower()
            try:
                validate_word(raw, language)
                guess = raw
            except (InvalidWordLengthError, WordNotFoundError) as e:
                click.echo(click.style(str(e), fg="red"))

        answer = None
        while answer is None:
            raw = click.prompt("Feedback").strip()
            try:
                validate_answer(raw)
                answer = raw
            except InvalidAnswerError as e:
                click.echo(click.style(str(e), fg="red"))

        click.echo(f"  {guess}  {_colored_answer(answer)}\n")

        if answer == Status.CORRECT * 5:
            click.echo(click.style(f"Solved! The word was: {guess}", fg="green", bold=True))
            break

        solver.add_step(guess, answer)
