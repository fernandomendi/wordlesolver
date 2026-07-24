FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
COPY core/ core/
COPY api/ api/

RUN uv sync --no-dev

EXPOSE 5000

CMD ["uv", "run", "flask", "--app", "api", "run", "--host", "0.0.0.0", "--port", "5000"]
