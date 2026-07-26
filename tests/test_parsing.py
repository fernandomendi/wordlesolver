import pytest

from core.models import Languages, Step
from core.parsing import parse_language, parse_steps


def test_parse_language_en():
    assert parse_language("en") == Languages.EN


def test_parse_language_es():
    assert parse_language("es") == Languages.ES


def test_parse_language_invalid():
    with pytest.raises(ValueError, match="Unsupported language"):
        parse_language("fr")


def test_parse_steps_from_cli_tuples():
    steps = parse_steps([("tares", "12221"), ("moust", "12211")])

    assert steps == [Step("tares", "12221"), Step("moust", "12211")]


def test_parse_steps_from_api_objects():
    steps = parse_steps([
        {"guess": "tares", "answer": "12221"},
        {"guess": "moust", "answer": "12211"},
    ])

    assert steps == [Step("tares", "12221"), Step("moust", "12211")]


def test_parse_steps_invalid_shape():
    with pytest.raises(ValueError, match="must be a list"):
        parse_steps("not-a-list")


def test_parse_steps_invalid_item():
    with pytest.raises(ValueError, match="must contain exactly 2 items"):
        parse_steps([("tares", "12221", "extra")])
