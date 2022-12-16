FROM node:18-alpine AS build

WORKDIR /slack-leaderboards/frontend

# install dependencies
ADD package.json yarn.lock ./
RUN yarn

# copy remaining files and build
COPY . .
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
