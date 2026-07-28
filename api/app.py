import os
from http import HTTPStatus

from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from api.routes import health_bp, solve_bp

DEFAULT_DEBUG = "false"
DEFAULT_PORT = "5000"
DEFAULT_FRONTEND_ORIGINS = "http://localhost:5173"


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["DEBUG"] = _to_bool(os.getenv("DEBUG", DEFAULT_DEBUG))
    app.config["PORT"] = int(os.getenv("PORT", DEFAULT_PORT))

    CORS(app, resources={r"/*": {"origins": _frontend_origins()}})

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


def _frontend_origins() -> list[str]:
    raw_origins = os.getenv("FRONTEND_ORIGINS", DEFAULT_FRONTEND_ORIGINS)
    origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    return origins or [DEFAULT_FRONTEND_ORIGINS]
