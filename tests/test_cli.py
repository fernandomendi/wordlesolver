import pytest
from click.testing import CliRunner
from cli.main import main


runner = CliRunner()


@pytest.mark.slow
def test_no_steps_en():
    result = runner.invoke(main, ["--lang", "en"])
    assert result.exit_code == 0
    assert len(result.output.strip()) == 5


@pytest.mark.slow
def test_no_steps_es():
    result = runner.invoke(main, ["--lang", "es"])
    assert result.exit_code == 0
    assert len(result.output.strip()) == 5


def test_known_steps_es():
    result = runner.invoke(main, ["--lang", "es", "--step", "careo", "12110", "--step", "recto", "11120"])
    assert result.exit_code == 0
    assert result.output.strip() == "greco"


def test_known_steps_en():
    result = runner.invoke(main, ["--lang", "en", "--step", "tares", "12221", "--step", "moust", "12211"])
    assert result.exit_code == 0
    assert result.output.strip() == "smith"


def test_invalid_guess():
    result = runner.invoke(main, ["--lang", "en", "--step", "zzzzz", "00000"])
    assert result.exit_code != 0
    assert "zzzzz" in result.output


def test_invalid_answer():
    result = runner.invoke(main, ["--lang", "en", "--step", "tares", "99999"])
    assert result.exit_code != 0
    assert "99999" in result.output
