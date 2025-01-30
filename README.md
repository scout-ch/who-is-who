# PBS Widget

## Environments

| Portainer App       | Branch | Domain                                        | Deployment |
|---------------------|--------|-----------------------------------------------|------------|
| gs-who-is-who       | main   | https://who-is-who.pbs.ch/                    | auto       |

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

The Docker image is automatically pushed to the [GitHub Docker
registry](https://github.com/scout-ch/who-is-who/pkgs/container/who-is-who) for
the `main` branch and git tags.

A webhook then triggers portainer to pull the image.
