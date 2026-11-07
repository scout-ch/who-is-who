import logging
import os
from collections import defaultdict

from flask import g

from app.core.codes import (
    APPNAME,
    DATA_FILE,
    DEFAULT_IMAGE,
    FIRSTNAME_LABEL,
    GROUPS_LABEL,
    ID_LABEL,
    IMAGE_LABEL,
    LASTNAME_LABEL,
    NAME_LABEL,
    NICKNAME_LABEL,
    PERSON_LABEL,
    ROLES_BY_GROUPS_LABEL,
    ROLES_LABEL,
    SUBGROUPS_LABEL,
)
from app.services.data import file
from app.services.etl.etl import run_etl

log = logging.getLogger(".".join((APPNAME, "Data")))


def get():
    if "data" not in g:
        if not os.path.isfile(DATA_FILE):
            # Only run after startup (no data file present yet)
            run_etl()
        g.data = file.read(DATA_FILE)
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
