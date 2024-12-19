# Slack Emoji Leaderboard
*Tracks emoji use to generate an emoji leaderboard for the MedShift slack*

## Setup / Deployment

### Backend
*The Slack Bot which tracks use and the API*
1. You'll need: [Python 3.10.x+](https://python.org) and [Poetry](https://python-poetry.org)
2. Change directories to the `backend` folder
3. To install dependencies, run `poetry install`
4. Create a `.env` file based off the `example.env`
5. Setup the database with `poetry run aerich upgrade`
   - If you use the `poetry shell` command you can ommit the `poetry run` prefix from these commands
6. To run the app you can do `poetry run python3 -m src.app`

### Frontend
*Simple frontend written in SvelteKit*
1. You'll need [Node 18+](https://nodejs.org/)
2. Change directories to the `frontend` folder
3. To install dependencies, run `yarn`
4. Create a `.env` file based off the `example.env`
5. Run `yarn dev` to run the frontend in dev mode

### Sync
*Discord bot which syncs the top emojis to a Discord server*
1. You'll need: [Python 3.10.x+](https://python.org) and [Poetry](https://python-poetry.org)
2. Change directories to the `sync` folder
3. To install dependencies, run `poetry install`
4. Create a `.env` file based off the `example.env`
5. To run the app you can do `poetry run python3 -m src.bot`

### Docker
- You'll need [Docker](https://docker.com/)
1. Create `backend/.env` based off `backend/example.env`
   - If you need to connect to the host machine, you can use `host.docker.internal`
1. Create a `frontend/.env`
2. Run `docker compose build` to build the image
3. Run `docker compose up -d` to start the app
- To view logs you can run `docker compose logs -f`

## Technologies
- [SvelteKit](https://kit.svelte.dev/)
- [Slack Bolt](https://slack.dev/bolt-python/concepts)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tortoise ORM](https://tortoise-orm.readthedocs.io/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Docker](https://docker.com/)
