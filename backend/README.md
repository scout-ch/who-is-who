# Who-Is-Who Backend

The who-is-who backend is responsible for processing the data from the hitobito instance. For PBS, this instance is the MiData instance hosted by Puzzle ITC.

The backend provides a REST Api with the following functions:

- Fetch data from a Hitobito instance
-

## Project Setup

### Install project dependencies

`pip install -r requirements.txt`

### Development

For development, it is recommended to use the docker compose setup defined on the top directory of the project.

### Environment variables

The following variables need to be set in order for the application to run:

`HITOBITO_TOKEN`, `HITOBITO_URL`, `SWIFT_AUTH_URL`, `SWIFT_USERNAME`, `SWIFT_PASSWORD`, `SWIFT_PROJECT`, `SWIFT_CONTAINER`, `SWIFT_REGION`, `ROOT_GROUP`.

The `ROOT_GROUP` defines the entrypoint for the data collection.
It corresponds the the `group_id` in the Hitobito instance of the group for which the who-is-who should be drawn.

## Structure

Loading and processing the data of the Hitobito instance follows the steps of an ETL pipeline: `extract.py`, `transform.py`, `load.py`. Extract fetches the data, transform simplifies it and load holds the functions for interfacing with the stored data.

`data.py` is used to interface with the transformed data. `configuration.py` provides the functionality to access the current configuration.
If no configuration overwrites are found, this defaults back to the values provided by `data.py`.

`renderer.py` renders the HTML data using jinja2 templates defined in `api/templates` and the configuration provided by `configuration.py`. The rendered data is then stored in the swift application set by the environment variables.

### Routes

Api routes are defined in the file `api/routes.py`.

| Endpoint                               | Method    | Parameters                                                                               | Description                                                                                                                                                                                                                  |
| -------------------------------------- | --------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/`                                    | GET       |                                                                                          | Index page. Returns the data used for generation.                                                                                                                                                                            |
| `/fetch-data`                          | GET       |                                                                                          | Causes server to fetch and prepare data from the configured hitobito instance.                                                                                                                                               |
| `/html/<string:locale>/<int:group_id>` | GET       | locale: `["de", "fr", "it"]` \\ group_id: `int`                                          | Access the html files generated with the root being the group of the given id. Language can be set with the locale.                                                                                                          |
| `/image/<string:person_id>`            | GET, POST | person_id: `string` of numbers, example `"1234"`                                         | Access or upload the profile image of the person with id person_id                                                                                                                                                           |
| `/config`                              | GET, POST | configuration json as specified by [configStore.js](/frontend/src/stores/configStore.js) | The configuration is used to overwrite, customize and expand on the hitobito instance data.                                                                                                                                  |
| `/static/styles.css`                   | GET       |                                                                                          | Static styling to be included in rendered pages.                                                                                                                                                                             |
| `/static/script.js`                    | GET       |                                                                                          | Static javascript to be included in rendered pages.                                                                                                                                                                          |
| `/render`                              | GET       |                                                                                          | Renders the static html site in all available locales based on the current configuration and stores it to the swift object storage. The rendered pages can be accessed via the `/html/<string:locale>/<int:group_id>` route. |
| `/download-zip`                        | GET       |                                                                                          | Returns a zip file containing the rendered html pages using the current configuration                                                                                                                                        |
