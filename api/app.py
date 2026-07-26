import os
from http import HTTPStatus

from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from api.routes import health_bp, solve_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["DEBUG"] = _to_bool(os.getenv("DEBUG", "false"))
    app.config["PORT"] = int(os.getenv("PORT", "5000"))

    CORS(
        app,
        resources={r"/*": {"origins": ["http://localhost:3000"]}},
    )

    app.register_blueprint(health_bp)
    app.register_blueprint(solve_bp)

    register_error_handlers(app)
    return app


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException) -> tuple[dict[str, str], int]:
        return (
            {
                "error": error.name,
                "message": error.description,
            },
            error.code or HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception) -> tuple[dict[str, str], int]:
        app.logger.exception("Unhandled exception in API", exc_info=error)
        return (
            {
                "error": HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
                "message": "An unexpected error occurred.",
            },
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


def _to_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}
