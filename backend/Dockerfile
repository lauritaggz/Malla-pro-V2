# Backend image for local development (docker compose). Not used in production yet (T-060).
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /usr/local/bin/uv

# The virtualenv lives outside /app/backend so the bind mount (and a host .venv, e.g. from
# Windows) never shadows it.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app/backend
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project

EXPOSE 8000
CMD ["uv", "run", "--no-sync", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
