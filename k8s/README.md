# Deployment on kubernetes

## Cronjob

The cronjob defined in `cronjob.yaml` refreshes the backend data (`transformed_data.json`) each night.

## Ingress

This project uses a traefik ingress configuration. The cluster you deploy to is expected to have a traefik ingress controller up and running. The ingress controller automatically provides HTTPS connections. The controller for this project can be found [here](https://github.com/scout-ch/tractor-k8s-ingress).

At a minimum, it is required to adjust the values `spec.rules.host` and `spec.tls.hosts` contained in `ingress.yaml`

## Secrets

Copy the file containing secrets: `cp secrets.example.yaml secrets.yaml` and fill in the correct values.

### NGINX BasicAuth

The nginx [default configuration](frontend/nginx/default.conf) assumes basic auth to be used to protect the website.
To create and push the credentials to your cluster, the following steps, taken from [kubernetes.github.io](https://kubernetes.github.io/ingress-nginx/examples/auth/basic/) are required:

1. Create a password file:

```sh
htpasswd -c auth foo
```

2. Convert it into a secret:

```sh
kubectl create secret generic basic-auth --from-file=auth
```

## Deploy

After configuring the basic auth, you can deploy to the cluster by running the command

```sh
kubectl apply -f secrets.yaml,backend.yaml,frontend.yaml,ingress.yaml,cronjob.yaml
```
