from http import HTTPStatus

from api import create_app


def test_health():
    client = create_app().test_client()

    response = client.get("/health")

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"status": "ok"}


def test_solve_happy_path():
    client = create_app().test_client()

    response = client.post(
        "/solve",
        json={"language": "en", "steps": [{"guess": "tares", "answer": "12221"}]},
    )

    assert response.status_code == HTTPStatus.OK
    assert set(response.json) == {"best_guess", "possible_words", "suggestions", "total_possible"}
    assert isinstance(response.json["best_guess"], str)
    assert isinstance(response.json["total_possible"], int)
    assert len(response.json["best_guess"]) == 5
    assert len(response.json["possible_words"]) <= 10
    assert len(response.json["suggestions"]) <= 10


def test_solve_bad_language():
    client = create_app().test_client()

    response = client.post("/solve", json={"language": "fr", "steps": []})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json["error"] == "Bad Request"


def test_solve_total_possible_zero():
    client = create_app().test_client()

    response = client.post(
        "/solve",
        json={
            "language": "en",
            "steps": [
                {"guess": "tares", "answer": "00000"},
                {"guess": "tares", "answer": "11111"},
            ],
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json["error"] == "Bad Request"
