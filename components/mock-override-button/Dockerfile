FROM python:3.12-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction

COPY src/ .

EXPOSE 8080
CMD ["python", "main.py"]
