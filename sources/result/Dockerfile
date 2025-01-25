# Multistages build
FROM node:latest AS build
WORKDIR /usr/src/app
# Only install production packages and use npm ci for security reason
COPY package*.json /usr/src/app/
RUN npm ci --omit=dev

FROM node:alpine3.21@sha256:15b885c5e195296ba49bab32681b478e92eb0f255078a84ad29020b87b0bdcc6 as prod
# Node.js doesn't support running as PID 1
RUN apk add dumb-init 
# Set environement variable for performance (express: https://expressjs.com/fr/advanced/best-practice-performance.html)
ENV NODE_ENV production
# Don't run the docker container as root
USER node
WORKDIR /usr/src/app
# Copy files and set permissions
COPY --chown=node:node --from=build /usr/src/app/node_modules /usr/src/app/node_modules
COPY --chown=node:node . /usr/src/app
CMD ["dumb-init", "node", "server.js"]
