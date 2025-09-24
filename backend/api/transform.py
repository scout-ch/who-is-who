from collections import defaultdict


def t(groups, roles, people):
    groups_by_id = {str(group["id"]): _transform_group(group) for group in groups}
    people_by_id = {str(person["id"]): person for person in people}
    roles_by_id = {
        str(role["id"]): _transform_role(
            role, people_by_id[str(role["attributes"]["person_id"])]
        )
        for role in roles
        if str(role["attributes"]["person_id"]) in people_by_id
    }

    subgroups_for_groups = _subgroups(groups)
    roles_for_groups = _roles_for_groups(roles, people_by_id)

    _clear_empty_groups(groups_by_id, subgroups_for_groups, roles_for_groups)

    return groups_by_id, subgroups_for_groups, roles_by_id, roles_for_groups


def _transform_group(group):
    # Attributes in group:
    name = group["attributes"]["name"]
    if not "parent_id" in group["attributes"]:
        return {
            "id": group["id"],
            "name": {"de": name, "fr": name, "it": name},
        }

    return {
        "id": group["id"],
        "name": {"de": name, "fr": name, "it": name},
        "parent_id": group["attributes"]["parent_id"],
    }


def _transform_role(role, person):
    # TODO: change as soon as human readable locale based roles are introduced to the JSON API
    name = role["attributes"]["type"].split(":")[-1]
    person = person["attributes"]
    return {
        "id": role["id"],
        "name": {"de": name, "fr": name, "it": name},
        "type": role["attributes"]["type"],
        "person": {
            "firstname": person["first_name"],
            "lastname": person["last_name"],
            "nickname": person["nickname"],
        },
    }


def _subgroups(groups):
    subgroups_for_group = defaultdict(list)
    for group in groups:
        if not "attributes" in group or not "parent_id" in group["attributes"]:
            continue
        parent_id = group["attributes"]["parent_id"]
        subgroups_for_group[str(parent_id)].append(str(group["id"]))
    return subgroups_for_group


def _roles_for_groups(roles, people_by_id):
    roles_for_groups = defaultdict(list)

    role_ids = set([r["id"] for r in roles])
    for role in roles:
        person_id = str(role["attributes"]["person_id"])
        group_id = str(role["attributes"]["group_id"])
        role_id = str(role["id"])

        # If the person_id does not point to a valid person, don't add it
        if person_id in people_by_id and role["id"] in role_ids:
            roles_for_groups[group_id].append(role_id)

            # ensure roles are not duplicated
            role_ids.remove(role_id)
    return roles_for_groups


def _clear_empty_groups(groups_by_id, subgroups_for_groups, roles_for_groups):
    # clear out empty groups
    empty_groups = _empty_groups(groups_by_id, subgroups_for_groups, roles_for_groups)
    while empty_groups:
        # remove empty groups
        groups_by_id = {k: v for k, v in groups_by_id.items() if k not in empty_groups}
        # recalculate subgroups
        subgroups_for_groups = _subgroups(groups_by_id.values())
        # identify newly empty groups
        empty_groups = _empty_groups(
            groups_by_id, subgroups_for_groups, roles_for_groups
        )


def _empty_groups(groups_by_id, subgroups_for_group, role_ids_for_group):
    ids = groups_by_id.keys()
    subgrouped = subgroups_for_group.keys()
    populated = role_ids_for_group.keys()

    return ids - (subgrouped | populated)
