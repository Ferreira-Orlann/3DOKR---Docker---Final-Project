# Multistages build
FROM node:latest AS build
WORKDIR /usr/local/result
# Only install production packages and use npm ci for security reason
COPY package*.json /usr/local/result
RUN npm ci --omit=dev

FROM node:18-alpine3.21@sha256:974afb6cbc0314dc6502b14243b8a39fbb2d04d975e9059dd066be3e274fbb25 as prod
# Node.js doesn't support running as PID 1
RUN apk add dumb-init 
# Set environement variable for performance (express: https://expressjs.com/fr/advanced/best-practice-performance.html)
ENV NODE_ENV production
# Don't run the docker container as root instead we use node's image built-in user
USER node
WORKDIR /usr/local/result
# Copy files and set permissions
COPY --chown=node:node --from=build /usr/local/result/node_modules /usr/local/result/node_modules
COPY --chown=node:node . /usr/local/result
CMD ["dumb-init", "node", "server.js"]
