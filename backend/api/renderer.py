from jinja2 import Environment, FileSystemLoader
import copy


def render_groups(
    groups_by_id,
    roles_by_id,
    subgroups_for_groups,
    roles_for_groups,
    root_name="",
    root_link="",
    locale="de",
    group_options={},
    role_options={},
):
    if isinstance(root_link, int):
        root_link = str(root_link) + ".html"
    elif root_link.split(".")[-1] != "html":
        root_link += ".html"

    group_pages = {}

    for id, group in groups_by_id.items():
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
            root=_root({locale: root_name}, root_link),
            group=_group_data(group, group_options),
            subgroups=subgroups,
            roles=roles,
            locale=locale,
        )

    return group_pages


def _sort_by_order(data, order):
    if any(entry["id"] not in order for entry in data):
        return data

    return sorted(data, key=lambda entry: order.index(entry["id"]))


def _root(name, link):
    return {"name": name, "place": link}


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

    return result


def _render_group(
    root,
    group,
    subgroups=[],
    roles=[],
    locale="de",
    templates_folder="api/templates",
    template_name="index.html.jinja",
):

    loader = FileSystemLoader(templates_folder)
    env = Environment(loader=loader)
    template = env.get_template(template_name)
    context = {
        "home": root,
        "group": group,
        "subgroups": subgroups,
        "roles": roles,
        "locale": locale,
    }
    return template.render(context)
