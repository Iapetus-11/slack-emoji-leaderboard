# slack-leaderboard
*Tracks emoji use to generate an emoji leaderboard for the MedShift slack*

## Setup / Deployment

### Backend
- You'll need: [Python 3.10.x+](https://python.org) and [Poetry](https://python-poetry.org)
1. Change directories to the `backend` folder
2. To install dependencies, run `poetry install`
3. Create a `.env` file based off the `example.env`
4. Setup the database with `poetry run aerich upgrade`
   - If you use the `poetry shell` command you can ommit the `poetry run` prefix from these commands
5. To run the bot you can do `poetry run python3 -m src.app`

### Frontend
- You'll need [Node 18+](https://nodejs.org/)
1. Change directories to the `frontend` folder
2. To install dependencies, run `yarn`
3. Create a `.env` file based off the `example.env`
4. Run `yarn dev` to run the frontend in dev mode

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
