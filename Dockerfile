FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libffi-dev python3-dev curl && apt-get clean

RUN pip install poetry

COPY . .

RUN poetry config virtualenvs.create false && poetry install --only main --no-root

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.asgi:app --host 0.0.0.0 --port 8000"]