FROM node:22 AS base
WORKDIR /usr/src/app

ARG VITE_BACKEND_URL
ENV VITE_BACKEND_URL=${VITE_BACKEND_URL}

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


###################################################
# Stage: prod-builder
# 
# Runs vite build and generates a static html/css/js site
# for distribution
###################################################
FROM base AS prod-builder
RUN npm run build

###################################################
# Stage: prod
# 
# Set up nginx to distribute the files
###################################################
FROM nginx AS prod

COPY --from=prod-builder /usr/src/app/dist /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]

