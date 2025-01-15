# PBS Widget

## Environments

| Deploio App         | Branch | Domain                                        | Deployment |
|---------------------|--------|-----------------------------------------------|------------|
| pbs-docker-widget   | main   | https://pbs-docker-widget.1c62958.deploio.app | auto       |

## Setup

```sh
git clone https://github.com/scout-ch/who-is-who.git
cd who-is-who

# Before running the setup script, make sure that you have docker installed and running
# Check .env for environment configuration (find in 1Password)
bin/setup
bin/check
```

## Run

```bash
# Run using simple rails app
bin/run
# Run using docker environment
bin/docker_run
```

## Deploying

The `main` branch is automatically deployed to `pbs-docker-widget` on Deploio (via Github connection).

Also a Docker image is automatically pushed to the [GitHub Docker
registry](https://github.com/scout-ch/who-is-who/pkgs/container/who-is-who) for
the `main` branch and git tags.
