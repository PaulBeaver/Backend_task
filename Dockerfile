FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /app

WORKDIR /app

COPY poetry-commerce/pyproject.toml poetry-commerce/poetry.lock ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry --version

RUN poetry config virtualenvs.create false && \
    poetry lock && \
    poetry install --without dev --no-root

COPY . .