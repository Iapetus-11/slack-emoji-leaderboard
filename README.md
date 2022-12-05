# slack-leaderboard
*Tracks emoji use to generate an emoji leaderboard for the MedShift slack*

## Setup
### Locally
- You'll need: [Python 3.10.x+](https://python.org) and [Poetry](https://python-poetry.org)
1. To install dependencies, run `poetry install`
2. Create a `.env` file based off the `example.env`
3. Setup the database with `poetry run aerich upgrade`
   - If you use the `poetry shell` command you can ommit the `poetry run` prefix from these commands
4. To run the bot you can do `poetry run python3 -m src.app`

### Docker
- You'll need [Docker](https://docker.com/)
1. Create a `.env` file based off the `example.env`
   - If you need to connect to the host machine, you can use `host.docker.internal`
2. Run `docker compose build` to build the image
3. Run `docker compose up -d` to start the app
- To view logs you can run `docker compose logs -f`

## Technologies
- [Slack Bolt](https://slack.dev/bolt-python/concepts)
- [Tortoise ORM](https://tortoise-orm.readthedocs.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://docker.com/)
