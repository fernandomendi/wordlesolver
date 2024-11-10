import json
from flask import Flask, request
import pandas as pd

from wordlesolver.core.variables import Language, Languages
from wordlesolver.filter import filter_words_accumulative
from wordlesolver.theory import best_guess


app = Flask(__name__)


@app.route("/best_guess", methods=["GET"])
def api_best_guess():
    language: Language = Languages().from_code(request.args["language"])
    steps: dict[str, str] = [
        {
            "guess": x.split(":")[0],
            "answer": x.split(":")[1]
        }
        for x in request.args["steps"].split(",")
    ]

    guess: str = best_guess(steps, language)
    return {
        "status": 200,
        "response": guess,
    }


@app.route("/possible_words", methods=["GET"])
def api_possible_words():
    language: Language = Languages().from_code(request.args["language"])
    steps: dict[str, str] = [
        {
            "guess": x.split(":")[0],
            "answer": x.split(":")[1]
        }
        for x in request.args["steps"].split(",")
    ]

    possible_words_df: pd.DataFrame = filter_words_accumulative(steps, language)
    possible_words: list[dict[str, str]] = json.loads(
        possible_words_df[["word", "probability"]]
        .to_json(orient="records")
    )
    return {
        "status": 200,
        "response": possible_words
    }


if __name__ == "__main__":
    app.run()
