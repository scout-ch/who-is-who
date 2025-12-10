import os
from collections import defaultdict
from logging import error

from flask import g

from api import extract, load, transform

DATA_FILE = "transformed_data.json"

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

    load.store_to_json(transformed_data)
    return transformed_data


def get(root_group="-1"):
    if root_group != "-1":
        g.root_group = root_group
    if "data" not in g:
        if not os.path.isfile(DATA_FILE):
            # Not the bestest solution, can be replaced with actual if there's time
            g.data = fetch_and_store(g.root_group)
        else:
            g.data = load.read_json(DATA_FILE)
    return g.data


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
