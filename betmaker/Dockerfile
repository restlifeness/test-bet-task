FROM python:3.12-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN python -m poetry config virtualenvs.create false \
    && python -m poetry install --no-root --no-dev

COPY . /app/

CMD ["sh", "./run.sh"]
