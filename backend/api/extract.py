import requests as re
import math
import os
import logging

from api.app import APPNAME

TOKEN = os.environ.get("MIDATA_TOKEN")
SCOUT_URL = os.environ.get("SCOUT_URL")

API_URL = f"{SCOUT_URL}/api" if SCOUT_URL else "/api"
HEADERS = {
    "X-Token": TOKEN,
    "accept": "*//",
    "Content-Type": "application/vnd.api+json",
}
GROUPS_FIELDS = ["id", "name"]
PEOPLE_FIELDS = ["first_name", "last_name", "nick_name"]
MAX_ID_FETCH = 600

log = logging.getLogger(".".join((APPNAME, "Extract")))


def api_fetch_organisation_data(org_id):
    # 0. fetch the org itself
    groups = [fetch_group(org_id)]

    # 1.  fetch all groups in the org
    # 1.1 fetch all direct children
    children = fetch_children_groups(org_id, org_id)

    # 1.2 fetch all children of children
    parents = []
    while children:
        child = children.pop()
        groups.append(child)
        parents.append(child["id"])

        if not children:
            children = fetch_children_groups(parents)
            parents.clear()

    # 2. fetch all roles in all groups
    group_ids = [group["id"] for group in groups]
    roles = fetch_roles_in_groups(group_ids)

    # 3. fetch all people belonging to any fetched roles
    people_ids = [role["attributes"]["person_id"] for role in roles]

    # Ensure the URL string won't be too long and trigger an 414
    # Splits the API call into n = #ids / MAX_ID_FETCH calls.
    # with stepsizes MAX_ID_FETCH.
    people = []
    if len(people_ids) > MAX_ID_FETCH:
        N = len(people_ids)
        nsteps = math.ceil(N / MAX_ID_FETCH)
        for i in range(nsteps):
            people.extend(
                fetch_people(
                    people_ids[i * MAX_ID_FETCH : min((i + 1) * MAX_ID_FETCH, N - 1)]
                )
            )
    else:
        people = fetch_people(people_ids)

    return groups, roles, people


def fetch_children_groups(group_ids, layer_group_id=None):
    if isinstance(group_ids, int):
        group_ids = str(group_ids)
    if not isinstance(group_ids, list):
        group_ids = [group_ids]

    filter = {"parent_id": ",".join(group_ids)}
    fields = {"groups": ["name", "display_name", "description", "parent_id"]}
    if layer_group_id:
        filter["layer_group_id"] = layer_group_id
    return api_load_all(endpoint="groups", fields=fields, filter=filter)


def fetch_group(group_id):
    return api_load(endpoint=f"groups/{group_id}", fields={"groups": ["name"]})


def fetch_roles_in_groups(group_ids):
    if isinstance(group_ids, list):
        group_ids = str(group_ids)[1:-1].replace(" ", "").replace("'", "")
    elif isinstance(group_ids, int):
        group_ids = str(group_ids)

    return api_load_all(
        endpoint="roles",
        fields={"roles": ["id", "person_id", "group_id", "type"]},
        filter={"group_id": group_ids},
    )


def fetch_people(ids):
    ids = str(ids)[1:-1].replace(" ", "")

    return api_load_all(
        endpoint="people",
        fields={"people": ["id", "first_name", "last_name", "nickname"]},
        filter={"id": ids},
    )


def api_load_all(endpoint="groups", locale="de", include=[], fields={}, filter={}):
    url = "/".join([API_URL, endpoint])
    params = api_params(locale, include, fields, filter)

    return _get_all_pages(url, params)


def api_load(endpoint="groups", locale="de", include=[], fields={}, filter={}):
    url = "/".join([API_URL, endpoint])
    params = api_params(locale, include, fields, filter)

    return _get(url, params)


def api_params(locale="de", include=[], fields={}, filter={}, page=1, pagesize=100):
    filterparams = {f"filter[{key}]": value for key, value in filter.items()}
    fieldparams = {f"fields[{key}]": ",".join(values) for key, values in fields.items()}

    params = {
        **filterparams,
        **fieldparams,
        "locale": locale,
        "page[number]": page,
        "page[size]": pagesize,
    }
    if len(include) > 0:
        params["include"] = ",".join(include)
    return params


def _response_ok(response):
    if response.status_code == re.codes.ok:
        return True
    log.error(f"[{response.status_code}]: {response.url}")
    return False


def _has_data(response):
    if "data" in response.json() and len(response.json()["data"]) > 0:
        return True
    log.error(f"No data field: {response.json()}")
    return False


def _get(url, params):
    response = re.get(url, headers=HEADERS, params=params)
    if not _response_ok(response) or not _has_data(response):
        return []

    return response.json()["data"]


def _get_all_pages(url, params):
    response = re.get(url, headers=HEADERS, params=params)
    if not _response_ok(response) or not _has_data(response):
        return []

    res = response.json()
    data = list(res["data"])

    while "next" in res["links"] and not res["links"]["self"] == res["links"]["last"]:
        res = re.get(SCOUT_URL + res["links"]["next"], headers=HEADERS)

        if not _response_ok(response) or not _has_data(response):
            return data

        res = res.json()

        data.extend(res["data"])

    return data
