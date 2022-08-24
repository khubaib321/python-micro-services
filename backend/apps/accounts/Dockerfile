FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV DOCKER_CONTAINER 1
ENV PYTHONFAULTHANDLER 1

RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get -y install build-essential libpq-dev \
  && pip install psycopg2-binary --no-binary psycopg2-binary

WORKDIR /src

COPY requirements.txt .
COPY . .

RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt
