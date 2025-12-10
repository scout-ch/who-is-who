# Who-Is-Who frontend

The who-is-who frontend connects to the backend and allows users to create a configuration of the data to be rendered.

On initial load, the frontend loads the data and the last configuration present on the backend and uses those values
to initialize the interface.

Data is persisted locally in the `dataStore` and the `configStore` using [pinia](https://pinia.vuejs.org/).

Icons are drawn with [oh-vue-icons](https://oh-vue-icons.js.org/) and [Heroicons](https://vue-hero-icons.netlify.app/)
[tailwindcss](https://tailwindcss.com/) is used for styling.

## Project Setup

```sh
npm install
```

### Development

For development, it is recommended to use the docker compose setup defined on the top directory of the project.

### API connection

The frontend is dependent on an active backend service.
While in development, routes to the api are configured in `vite.config.js`.
When deployed, a nginx configured with `nginx/default.conf` is expected to create a proxy pass to the backend.
Examples of how the deployment can be handled are found in the `docker-compose.yaml` file or the kubernetes deploy scripts `k8s/frontend.yaml, k8s/ingress.yaml`.

More configuration is not needed for the frontend.

## Project Structure

The project recursivly renders the data gathered from the backend into interactive elements.
Next to that, it shows a view of the currently rendered HTML on the server.

The vue entrypoint is the `HomeView` which then adds the groups as well as the preview.
For each groups, it is checked if there are any subgroups. If so, these are added.
Otherwise, the people contained in the group are added.

Rendering the frontend follows this order:

`HomeView.vue` -> `Groups.vue` -> `Group.vue` -> ... -> `Group.vue` -> `RoleContainer.vue` -> `Role.vue` -> `RoleDetail.vue`
