FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder
WORKDIR /app

COPY README.md pyproject.toml uv.lock ./
COPY src/backend/__init__.py ./src/backend/
RUN uv sync


FROM python:3.13-alpine AS runner
WORKDIR /app

COPY --from=builder /app/.venv ./.venv
COPY src/backend ./src/backend
COPY src/main.py ./src/

CMD [ ".venv/bin/python", "src/main.py" ]

