FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder
WORKDIR /app

COPY README.md pyproject.toml uv.lock ./
COPY src/app/__init__.py ./src/app/
RUN uv sync


FROM python:3.13-alpine AS runner
WORKDIR /app

COPY --from=builder /app/.venv ./.venv
COPY src ./src/

CMD [ ".venv/bin/python", "src/main.py" ]

