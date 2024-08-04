FROM python:3.12

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN python -m poetry config virtualenvs.create false \
    && python -m poetry install --no-root --no-dev

COPY . /app/

CMD ["python", "-m", "dramatiq", "-p", "1", "-t", "1", "src.jobs"]
