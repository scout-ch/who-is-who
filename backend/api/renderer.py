from jinja2 import Environment, FileSystemLoader
import copy
import logging

from api.app import APPNAME

log = logging.getLogger(".".join((APPNAME, "Renderer")))


def render_groups(
    groups_by_id,
    roles_by_id,
    subgroups_for_groups,
    roles_for_groups,
    root_name="",
    root_id=0,
    locale="de",
    link_prefix="",
    group_options={},
    role_options={},
    images=[],
    stylesheet="styles.css",
    flat=False,
):
    group_pages = {}
    for id in _groups_to_render(
        str(root_id), subgroups_for_groups, group_options["exclude"]
    ):
        if id in group_options["exclude"]:
            continue

        subgroups = []
        roles = []

        if id in subgroups_for_groups:
            subgroups = [
                _group_data(groups_by_id[subgroup_id], group_options)
                for subgroup_id in subgroups_for_groups[id]
                if subgroup_id in groups_by_id
                and not subgroup_id in group_options["exclude"]
            ]

            if id in group_options["order"]:
                subgroups = _sort_by_order(subgroups, group_options["order"][id])

        elif id in roles_for_groups:
            roles = [
                _role_data(roles_by_id[role_id], role_options)
                for role_id in roles_for_groups[id]
                if role_id in roles_by_id and not role_id in role_options["exclude"]
            ]

            if id in role_options["order"]:
                roles = _sort_by_order(roles, role_options["order"][id])

        group_pages[id] = _render_group(
            root_name=root_name,
            root_id=root_id,
            group=_group_data(groups_by_id[id], group_options),
            subgroups=subgroups,
            roles=roles,
            images=images,
            link_prefix=link_prefix,
            locale=locale,
            stylesheet=stylesheet,
            flat=flat,
        )

    return group_pages


def _groups_to_render(root_group: int, subgroups_for_groups: {}, to_exclude=[]):
    groups_to_process = copy.deepcopy(subgroups_for_groups[root_group])
    result = [root_group]
    while groups_to_process:
        current_group = groups_to_process.pop()
        if current_group in to_exclude:
            continue

        result.append(current_group)
        if current_group in subgroups_for_groups:
            groups_to_process.extend(subgroups_for_groups[current_group])
    return result


def _sort_by_order(data, order):
    if any(entry["id"] not in order for entry in data):
        return data

    return sorted(data, key=lambda entry: order.index(entry["id"]))


def _root(name, group_id):
    return {"name": name, "group_id": group_id}


def _option_overwrite(data, options, id, label):
    if label not in data or label not in options or id not in options[label]:
        return data

    for locale, value in options[label][id].items():
        data[label][locale] = value


def _group_data(group, group_options):
    id = group["id"]
    result = copy.deepcopy(group)

    _option_overwrite(result, group_options, id, "description")
    _option_overwrite(result, group_options, id, "name")

    return result


def _role_data(role, role_options):
    # Structure should be like:
    #    {
    #        "name": {
    #            "de": role_name,
    #            "fr": role_name,
    #            "it": role_name,
    #         },
    #        "type": role_type,
    #        "person": {
    #            "firstname": first_name,
    #            "lastname": last_name,
    #            "nickname": nickname,
    #        },
    #    }
    id = role["id"]
    result = copy.deepcopy(role)

    _option_overwrite(result, role_options, id, "name")

    if id in role_options["tel"]:
        result["tel"] = role_options["tel"][id]

    if id in role_options["email"]:
        result["email"] = role_options["email"][id]

    return result


def _render_group(
    root_name,
    root_id,
    group,
    subgroups=[],
    roles=[],
    locale="de",
    images=[],
    flat=False,
    link_prefix="",
    templates_folder="templates",
    template_name="index.html.jinja",
    stylesheet="styles.css",
):

    loader = FileSystemLoader(templates_folder)
    env = Environment(loader=loader)
    template = env.get_template(template_name)
    context = {
        "root_name": root_name,
        "root_id": root_id,
        "group": group,
        "subgroups": subgroups,
        "roles": roles,
        "images": images,
        "link_prefix": link_prefix,
        "locale": locale,
        "stylesheet": stylesheet,
        "flat": flat,
    }
    return template.render(context)
