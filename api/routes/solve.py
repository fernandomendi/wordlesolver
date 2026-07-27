from http import HTTPStatus

from flask import Blueprint, request
from werkzeug.exceptions import BadRequest

from core import Solver, parse_language, parse_steps

solve_bp = Blueprint("solve", __name__)


@solve_bp.post("/solve")
def solve() -> tuple[dict[str, object], int]:
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        raise BadRequest("Request body must be a JSON object.")

    try:
        language = parse_language(payload.get("language"))
        steps = parse_steps(payload.get("steps"))
    except ValueError as error:
        raise BadRequest(str(error)) from error

    solver = Solver(language)
    for step in steps:
        try:
            solver.add_step(step.guess, step.answer)
        except ValueError as error:
            raise BadRequest(str(error)) from error

    total_possible = solver.total_possible()
    # Contradictory feedback should be surfaced as a client error.
    if total_possible == 0:
        raise BadRequest("No possible words remaining. Check your feedback.")

    return (
        {
            "best_guess": solver.best_guess(),
            "possible_words": [
                {"word": entry["word"], "probability": entry["probability"]}
                for entry in solver.possible_words()
            ],
            "suggestions": solver.suggestions(),
            "total_possible": total_possible,
        },
        HTTPStatus.OK,
    )
