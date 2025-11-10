import itertools

from jinja2 import Environment, FileSystemLoader

from api import configuration, data

TEMPLATE_FOLDER = "templates"

NAME_LABEL = "name"


def render_group(
    locale: str,
    root_id: str,
    render_root=False,
    render_subgroups=True,
    render_people=True,
) -> str:

    context = {
        "locale": locale,
        "render_root": render_root,
        "render_subgroups": render_subgroups,
        "render_people": render_people,
        "root_id": root_id,
        "layers": _collect_layers(root_id),
        # Collect all groups below the given group id
        "groups": _collect_groups(_collect_nested_ids(root_id) + [root_id]),
    }
    result = _render_template("root_group.html.jinja", context)

    return result


def _collect_nested_ids(group_id):
    return list(set(itertools.chain(*_collect_subgroups(group_id).values())))


def _collect_layers(group_id, layer=1):
    layers = {group_id: f"{layer}"}
    for id in configuration.subgroups(group_id):
        layers.update(_collect_layers(id, layer + 1))
    return layers


def _collect_subgroups(group_id):
    subgroups = {group_id: configuration.subgroups(group_id)}

    for id in subgroups[group_id]:
        subgroups[id] = configuration.subgroups(id)
        subgroups.update(_collect_subgroups(id))

    return subgroups


def _collect_groups(group_ids, render_subgroups=True, render_people=True):
    return {
        id: _collect_group_data(id, render_subgroups, render_people) for id in group_ids
    }


def _collect_group_data(group_id, render_subgroups=True, render_people=True):
    people = []
    if render_people:
        roles = configuration.roles_by_group(group_id)
        people = [configuration.person_data(role_id) for role_id in roles]

    has_subgroups = group_id in data.subgroups()
    subgroups = []
    if render_subgroups and has_subgroups:
        subgroups = configuration.subgroups(group_id)

    return {
        "id": group_id,
        "name": configuration.group_name(group_id),
        "description": configuration.group_description(group_id),
        "people": people,
        "subgroups": subgroups,
    }


def html_start(stylesheet_link="") -> str:
    stylesheet_content = ""
    with open("api/static/styles.css") as f:
        stylesheet_content = f.read()

    context = {
        "stylesheet_link": stylesheet_link,
        "stylesheet_content": stylesheet_content,
    }
    return _render_template("html_start.html.jinja", context)


def html_end(js_link="") -> str:
    js_content = ""
    with open("api/static/script.js") as f:
        js_content = f.read()

    context = {"js_content": js_content, "js_link": js_link}
    return _render_template("html_end.html.jinja", context)


def _render_subgroups(locale: str, group_id: str) -> str:
    return "".join(
        [
            render_group(locale, subgroup)
            for subgroup in configuration.subgroups(group_id)
        ]
    )


def _render_template(template_name, context) -> str:
    loader = FileSystemLoader(TEMPLATE_FOLDER)
    env = Environment(loader=loader)
    template = env.get_template(template_name)

    return template.render(context)
