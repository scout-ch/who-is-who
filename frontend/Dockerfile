FROM node:22 AS base
WORKDIR /usr/local/app

COPY package.json package-lock.json ./
RUN npm install
COPY index.html vite.config.js jsconfig.json ./
COPY public ./public
COPY src ./src

###################################################
# Stage: dev
# 
# This stage is used for development of the client application. It sets 
# the default command to start the Vite development server.
###################################################
FROM base AS dev
CMD ["npm", "run", "dev"]
