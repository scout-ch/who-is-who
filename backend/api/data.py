import os
from collections import defaultdict
import logging

from flask import g

from api import extract, load, transform

from api.health import write_data_load_timestamp, write_last_login_result, write_data_transformation_result

DATA_FOLDER = "data"
DATA_FILE = '/'.join([DATA_FOLDER, "transformed_data.json"])

# Use Javascript conventions for JSON tags
GROUPS_LABEL = "groups"
ROLES_LABEL = "roles"
SUBGROUPS_LABEL = "subgroups"
ROLES_BY_GROUPS_LABEL = "rolesByGroups"
NAME_LABEL = "name"
IMAGE_LABEL = "images"

PERSON_LABEL = "person"
FIRSTNAME_LABEL = "firstname"
LASTNAME_LABEL = "lastname"
NICKNAME_LABEL = "nickname"
ID_LABEL = "id"

DEFAULT_IMAGE = "default_image"

ROOT_GROUP = ROOT_GROUP = str(
    os.environ.get("ROOT_GROUP") if os.environ.get("ROOT_GROUP") else "0"
)


def fetch_and_store(root_group: str):
    groups, roles, people = extract.api_fetch_organisation_data(root_group)
    groups_by_id, subgroups_for_groups, roles_by_id, roles_for_groups, images = (
        transform.t(groups, roles, people)
    )
    transformed_data = {
        GROUPS_LABEL: groups_by_id,
        SUBGROUPS_LABEL: subgroups_for_groups,
        ROLES_LABEL: roles_by_id,
        ROLES_BY_GROUPS_LABEL: roles_for_groups,
        IMAGE_LABEL: images,
    }

    load.store_to_json(transformed_data, DATA_FILE)
    return transformed_data


def get():
    if "data" not in g:
        if not os.path.isfile(DATA_FILE):
            # Not the bestest solution, can be replaced with actual if there's time
            try_load()
        else:
            g.data = load.read_json(DATA_FILE)
    return g.data

def try_load():
    try:
        logging.info("Loading root group")
        result = fetch_and_store(ROOT_GROUP)
    except ConnectionError as ce:
        write_last_login_result("failed")
        logging.error(str(ce))
        return ["error"], 500
    except RuntimeError as re:
        write_data_transformation_result("failed")
        logging.error(str(re))
        return ["error"], 500
    except Exception as e:
        logging.error(str(e))
        return ["error"], 500


    write_data_transformation_result("successful")
    write_last_login_result("successful")
    write_data_load_timestamp()

    g.data = result

    return ["success"], 200


def groups():
    return _get_dict(GROUPS_LABEL)


def group_names(group_id):
    return groups()[group_id][NAME_LABEL]


def roles():
    return _get_dict(ROLES_LABEL)


def role_names(role_id):
    return roles()[role_id][NAME_LABEL]


def firstname(role_id):
    return roles()[role_id][PERSON_LABEL][FIRSTNAME_LABEL]


def lastname(role_id):
    return roles()[role_id][PERSON_LABEL][LASTNAME_LABEL]


def nickname(role_id):
    return roles()[role_id][PERSON_LABEL][NICKNAME_LABEL]


def person_id(role_id):
    return roles()[role_id][PERSON_LABEL][ID_LABEL]


def person_name(role_id):
    fname = firstname(role_id)
    lname = lastname(role_id)

    fname = fname if fname else ""
    lname = lname if lname else ""
    nname = nickname(role_id)
    nname = " / " + nname if nname else ""
    return fname + " " + lname + nname


def get_default_dict(label):
    return defaultdict(list, _get_dict(label))


def subgroups():
    return get_default_dict(SUBGROUPS_LABEL)


def roles_by_group() -> dict:
    return get_default_dict(ROLES_BY_GROUPS_LABEL)


def images():
    return _get_dict(IMAGE_LABEL)


def image(role_id):
    p_id = person_id(role_id)
    imgs = images()
    if p_id in imgs:
        return imgs[p_id]
    return DEFAULT_IMAGE


def _get_dict(label):
    data = get()
    if label in data:
        return data[label]
    return {}
