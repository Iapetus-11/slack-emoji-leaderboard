FROM node:18-alpine AS build

# make necessary directories and copy over files
WORKDIR /slack-leaderboards/frontend
COPY . .

# install dependencies & build
RUN yarn
RUN yarn build

FROM node:18-alpine AS deploy

WORKDIR /slack-leaderboards/frontend

RUN rm -rf ./*

# copy over necessary files from build stage
COPY --from=build /slack-leaderboards/frontend/package.json .
COPY --from=build /slack-leaderboards/frontend/build .

# install prod dependencies
RUN yarn --prod

CMD ["node", "index.js"]
