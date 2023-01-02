FROM node:18-alpine AS build

WORKDIR /slack-emoji-leaderboard/frontend

# install dependencies
ADD package.json yarn.lock ./
RUN yarn

# copy remaining files and build
COPY . .
RUN yarn build

FROM node:18-alpine AS deploy

WORKDIR /slack-emoji-leaderboard/frontend

RUN rm -rf ./*

# copy over necessary files from build stage
COPY --from=build /slack-emoji-leaderboard/frontend/package.json .
COPY --from=build /slack-emoji-leaderboard/frontend/build .

# install prod dependencies
RUN yarn --prod

CMD ["node", "index.js"]
