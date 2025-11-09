from jinja2 import Environment, FileSystemLoader

from api import configuration, data

TEMPLATE_FOLDER = "templates"

NAME_LABEL = "name"


def render_group(
    locale: str,
    group_id: str,
    layer: int = 1,
    render_group_head=True,
    render_subgroups=True,
    render_people=True,
) -> str:
    group_name = data.groups()[group_id][NAME_LABEL]
    group_description = configuration.group_description(group_id)

    context = {
        "layer": layer,
        "locale": locale,
        "group_id": group_id,
        "name": group_name,
        "description": group_description,
        "render_group_head": render_group_head,
    }

    if render_people and not group_id in data.subgroups():
        roles = configuration.roles_by_group(group_id)
        people = [configuration.person_data(role_id) for role_id in roles]
        context["people"] = people

    result = _render_template("group_data.html.jinja", context)

    if render_subgroups and group_id in data.subgroups():
        return result + _render_subgroups(locale, group_id, layer)

    return result


def html_start(stylesheet_link="") -> str:
    stylesheet_content = ""
    with open("api/styles.css") as f:
        stylesheet_content = f.read()

    context = {
        "stylesheet_link": stylesheet_link,
        "stylesheet_content": stylesheet_content,
    }
    return _render_template("html_start.html.jinja", context)


def html_end(js_link="") -> str:
    js_content = ""
    with open("api/script.js") as f:
        js_content = f.read()

    context = {"js_content": js_content, "js_link": js_link}
    return _render_template("html_end.html.jinja", context)


def _render_subgroups(locale: str, group_id: str, layer: int) -> str:
    return "".join(
        [
            render_group(locale, subgroup, layer + 1)
            for subgroup in configuration.subgroups(group_id)
        ]
    )


def _render_template(template_name, context) -> str:
    loader = FileSystemLoader(TEMPLATE_FOLDER)
    env = Environment(loader=loader)
    template = env.get_template(template_name)

    return template.render(context)
