FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=TRUE

## install essential packages
#RUN apt-get update -y
#RUN apt-get install -y git build-essential libgl1 libglib2.0-0 ffmpeg

# install & configure poetry
RUN python3 -m pip install poetry --no-cache-dir
RUN poetry config virtualenvs.in-project true

# make necessary dir
RUN mkdir slack-leaderboards
WORKDIR /slack-leaderboards

# install dependencies
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-dev --no-interaction

# copy over necessary folders
COPY src src
COPY migrations migrations

# run app
CMD poetry run python3 -m src.app
