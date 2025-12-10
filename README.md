# Who-is-who

Collects information from a hitobito pbs instance and uses the information to generate a list of group members.
Users can customize the lists appearance using the frontend.

The project consist of a python backend and a javascript frontend. To store blob data, a swift object storage is used.

## Development

Clone the github repository.

```
git clone git@github.com:scout-ch/who-is-who.git;

```

### Docker

Move the `.example.env` file to `.env` and replace its values.

The docker-compose file creates a local frontend, backend and swift container.

#### Creating a local swift container

To create a local swift container, an adjusted copy of the [docker-keystone-swift](https://github.com/CSCfi/docker-keystone-swift) repository is needed.

1. Move to the directory containing the who-is-who project
1. `git clone git@github.com:CSCfi/docker-keystone-swift.git`
2. Add the arguments `OS_AUTH_URL`, `OS_SWIFT_URL`

```sh
sed -i '8i\
ARG         OS_AUTH_URL\
ARG         OS_SWIFT_URL' Dockerfile

```

3. Change the `OS_SWIFT_URL`: `sed -i '/OS_SWIFT_URL=/s/0.0.0.0/swift/' Dockerfile`

After that, the containers are started with the regular `docker-compose up` commands.

### Frontend

The frontend provides a user interface to configure the static generation of the who-is-who.
It is based on [vue](https://vuejs.org/), uses [vite](https://vite.dev/) to build, and [tailwind](https://tailwindcss.com/) for css styling.

For frontend development, go [here](frontend/README.md).

### Backend

The backend fetches the data used for the generation and generates the static page.
The server is built with [flask](https://flask.palletsprojects.com/en/stable/) and the generation with [jinja2](https://jinja.palletsprojects.com/en/stable/).

For backend development, go [here](backend/README.md).

## Deployment

The webapp is deployed to a kubernetes cluster. The steps to achieve this are documented [here](k8s/README.md).

The frontend is compiled by vite and then served by an [nginx](https://nginx.org/index.html).
The configuration for said nginx lives [here](frontend/nginx/default.conf)
