FROM python:3.10.6-slim-buster

WORKDIR /app

RUN apt update && \
    apt install make && \
    rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir pipenv && \
    pipenv install --system && \
    pip uninstall -y pipenv && \
    rm -rf Pipfile*

COPY main.py main.py
COPY ./src ./src