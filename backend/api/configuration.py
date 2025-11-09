import os

from flask import g

from api import data, load

CONFIG_FILE = "config.json"

GROUPS_LABEL = "groups"
ROLES_LABEL = "roles"
EXCLUDE_LABEL = "exclude"
DESCRIPTION_LABEL = "description"
NAME_LABEL = "name"
ORDER_LABEL = "order"
EMAIL_LABEL = "email"
TEL_LABEL = "tel"
IMAGES_LABEL = "images"


def get():
    if "configuration" not in g:
        if not os.path.isfile(CONFIG_FILE):
            # Create empty defaults if no config file exists
            config = {
                GROUPS_LABEL: {
                    EXCLUDE_LABEL: [],
                    DESCRIPTION_LABEL: {},
                    NAME_LABEL: {},
                    ORDER_LABEL: {},
                },
                ROLES_LABEL: {
                    EXCLUDE_LABEL: [],
                    NAME_LABEL: {},
                    ORDER_LABEL: {},
                    TEL_LABEL: {},
                    EMAIL_LABEL: {},
                },
                IMAGES_LABEL: {},
            }
            load.store_to_json(config, CONFIG_FILE)
            g.configuration = config
        else:
            g.configuration = load.read_json(CONFIG_FILE)
    g.configuration = check_and_correct_config(g.configuration)
    return g.configuration


def set_config(config):
    config = check_and_correct_config(config)
    g.configuration = config
    load.store_to_json(config, CONFIG_FILE)


def excluded_groups():
    return get()[GROUPS_LABEL][EXCLUDE_LABEL]


def excluded_roles() -> list:
    return get()[ROLES_LABEL][EXCLUDE_LABEL]


def roles_by_group(group_id) -> list:
    """Return roles of the given group ID, according to the order specified by the user and only if they have not been specified as excluded.

    Parameters
    ----------
    group_id : group ID in the original database
        This id should have been set by extract.py

    Returns
    -------
    list
        Ordered roles to be included

    """
    return [
        role
        for role in _order(group_id, ROLES_LABEL, data.ROLES_BY_GROUPS_LABEL)
        if role not in excluded_roles()
    ]


def group_description(group_id):
    descriptions = get()[GROUPS_LABEL][DESCRIPTION_LABEL]
    if group_id in descriptions:
        return descriptions[group_id]
    return None


def group_name(group_id=""):
    group_names = get()[GROUPS_LABEL][NAME_LABEL]
    if group_id == "":
        return group_names

    if group_id in group_names:
        return group_names[group_id]
    # If no configuration exists for the given group, return the default data
    return data.groups()[group_id][NAME_LABEL]


def subgroups(group_id) -> list:
    """Return subgroups of the given group ID, according to the order specified by the user and only if they have not been specified as excluded.

    Parameters
    ----------
    group_id : group ID in the original database
        This id should have been set by extract.py

    Returns
    -------
    list
        Ordered subgroups to be included

    """
    return [
        subgroup
        for subgroup in _order(group_id, GROUPS_LABEL, data.SUBGROUPS_LABEL)
        if subgroup not in excluded_groups()
    ]


def _order(group_id, configuration_label, data_label=None):
    orders = get()[configuration_label][ORDER_LABEL]
    if group_id in orders:
        return orders[group_id]
    if data_label:
        return data.get_default_dict(data_label)[group_id]
    return data.get_default_dict(configuration_label)[group_id]


def person_data(role_id):
    return {
        "role_id": role_id,
        "role_name": role_name(role_id),
        "role_emails": role_email(role_id),
        "role_tel": role_tel(role_id),
        "image": image(role_id),
        "person_name": data.person_name(role_id),
    }


def image(role_id: str) -> str:
    images = get()[IMAGES_LABEL]
    person_id = data.person_id(role_id)
    if person_id in images:
        return images[person_id]
    return data.image(role_id)


def images() -> list[str]:
    return get()[IMAGES_LABEL]


def role_name(role_id=""):
    role_names = get()[ROLES_LABEL][NAME_LABEL]
    if role_id == "":
        return role_names
    if role_id in role_names:
        return role_names[role_id]
    return data.role_names(role_id)


def role_orders(group_id):
    orders = get()[ROLES_LABEL][ORDER_LABEL]
    if group_id in orders:
        return orders[group_id]
    return data.roles_by_group()[group_id]


def role_tel(role_id):
    tels = get()[ROLES_LABEL][TEL_LABEL]
    if role_id in tels:
        return tels[role_id]
    return None


def role_email(role_id):
    email = get()[ROLES_LABEL][EMAIL_LABEL]
    if role_id in email:
        return email[role_id]
    return None


def check_and_correct_config(config):
    if len(config) == 0:
        return config

    subgroups_for_group = data.subgroups()
    roles_for_groups = data.roles_by_group()

    # Check groups.order entries to contain valid maps
    # Valid means that every subgroup must be present in the config map
    _ensure_valid_mappings(config, subgroups_for_group, GROUPS_LABEL)

    # Same goes for roles.order
    _ensure_valid_mappings(config, roles_for_groups, ROLES_LABEL)

    return config


def _ensure_valid_mappings(config, data, config_label):
    # Ensure that customized orders include a mapping for all data members,
    # even after fetching and a group/role has been added/removed.
    for id, order in config[config_label][ORDER_LABEL].items():
        # Check that all mapped entities exist
        valid_entities = [entity_id for entity_id in order if entity_id in data[id]]
        order.clear()
        order.extend(valid_entities)

        # Check all entities that should be mapped are mapped
        for entity in data[id]:
            if not entity in order:
                order.append(entity)
