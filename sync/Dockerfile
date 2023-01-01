FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=TRUE

# install & configure poetry
RUN python3 -m pip install poetry --no-cache-dir
RUN poetry config virtualenvs.in-project true

WORKDIR /slack-emoji-leaderboard/sync

# install dependencies
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-dev --no-interaction

# copy over necessary folders
COPY src src

# run app
CMD poetry run python3 -m src.app
