FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libffi-dev python3-dev curl && apt-get clean

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --with dev --no-root

COPY app/ ./app/
COPY migrations/ ./migrations/
COPY alembic.ini ./

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.asgi:app --host 0.0.0.0 --port 8000"]