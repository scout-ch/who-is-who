from flask import (
    Response,
    Blueprint,
    request,
    jsonify,
    send_file,
)
import zipfile
from io import BytesIO
import os
import logging


from . import extract, transform, load, renderer

from api.app import APPNAME

log = logging.getLogger(".".join((APPNAME, "Renderer")))

bp = Blueprint("/", __name__)

PBS_GROUP = 2
CONFIG_DATA = "config.json"

DATA_FILE = "transformed_data.json"
CONFIG_FILE = "config.json"


@bp.route("/", methods=["GET"])
def index():
    if not os.path.isfile(DATA_FILE):
        fetch_data()

    data = load.read_json(DATA_FILE)
    groups_by_id = data["groups_by_id"]
    roles_by_id = data["roles_by_id"]
    subgroups_for_group = data["subgroups_for_groups"]
    roles_for_groups = data["roles_for_groups"]

    return jsonify(
        {
            "groups": groups_by_id,
            "subgroups_for_groups": subgroups_for_group,
            "roles": roles_by_id,
            "roles_for_groups": roles_for_groups,
        }
    )


@bp.route("/html/<string:locale>/<int:group_id>", methods=["GET"])
def get_html(locale, group_id):
    try:
        html = load.get_html(group_id, locale)
        return html.decode()
    except Exception as e:
        return {"error": str(e)}, 404


@bp.route("/<path:prefix>/styles.css", methods=["GET"])
def get_style(prefix):
    return send_file("styles.css")


@bp.route("/image/<string:person_id>", methods=["GET"])
def get_image(person_id):
    try:
        obj, image = load.get_image(person_id)
        return Response(image, mimetype=obj.content_type)
    except Exception as e:
        return {"error": str(e)}, 404


@bp.route("/image-upload/<string:person_id>", methods=["POST"])
def image_upload(person_id):
    file = request.files["image"]
    filename = load.upload_image(file, person_id)
    return {"filename": filename}


@bp.route("/fetch_data", methods=["GET"])
def fetch_data():
    groups, roles, people = extract.api_fetch_organisation_data(PBS_GROUP)
    # groups, roles, people = load.read_json("data.json") # uncomment for testing purposes
    groups_by_id, subgroups_for_groups, roles_by_id, roles_for_groups = transform.t(
        groups, roles, people
    )
    load.store_to_json(
        {
            "groups_by_id": groups_by_id,
            "subgroups_for_groups": subgroups_for_groups,
            "roles_by_id": roles_by_id,
            "roles_for_groups": roles_for_groups,
        }
    )
    return jsonify({"result": "success"})


@bp.route("/render", methods=["GET"])
def render():
    config = load.read_json(CONFIG_FILE)

    data = load.read_json(DATA_FILE)
    groups_by_id = data["groups_by_id"]
    roles_by_id = data["roles_by_id"]
    subgroups_for_group = data["subgroups_for_groups"]
    roles_for_groups = data["roles_for_groups"]

    for locale in ["de", "fr", "it"]:
        group_pages = renderer.render_groups(
            groups_by_id=groups_by_id,
            roles_by_id=roles_by_id,
            subgroups_for_groups=subgroups_for_group,
            roles_for_groups=roles_for_groups,
            root_name="PBS",
            root_id=PBS_GROUP,
            locale=locale,
            group_options=config["groups"],
            role_options=config["roles"],
            link_prefix="/api/html/",
            images=config["images"],
            stylesheet="styles.css",
            flat=False,
        )
        for key in group_pages:
            load.upload_html(key, locale, group_pages[key])
        log.info(f"stored {len(group_pages)} files for locale {locale}")

    return jsonify(group_pages)


@bp.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        data = request.get_json()["data"]
        load.store_to_json(data, CONFIG_FILE)
        return jsonify("success")
    elif request.method == "GET":
        return jsonify(load.read_json(CONFIG_FILE))


@bp.route("/download-zip")
def download_zip():
    memory_file = BytesIO()

    config = load.read_json(CONFIG_FILE)

    data = load.read_json(DATA_FILE)
    groups_by_id = data["groups_by_id"]
    roles_by_id = data["roles_by_id"]
    subgroups_for_group = data["subgroups_for_groups"]
    roles_for_groups = data["roles_for_groups"]

    pages = {}
    locales = ["de", "fr", "it"]
    for locale in locales:
        group_pages = renderer.render_groups(
            groups_by_id=groups_by_id,
            roles_by_id=roles_by_id,
            subgroups_for_groups=subgroups_for_group,
            roles_for_groups=roles_for_groups,
            root_name="PBS",
            root_id=PBS_GROUP,
            locale=locale,
            group_options=config["groups"],
            role_options=config["roles"],
            images=config["images"],
            flat=True,
            stylesheet="../styles.css",
        )
        for key in group_pages:
            pages[f"{locale}/{key}.html"] = group_pages[key]

    with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add html pages
        for filename, html in pages.items():
            zf.writestr(filename, html)
        # Add styles.css
        zf.write("api/styles.css", "styles.css")
        # Add images
        zf.write("api/static/favicon.png", "img/logo.png")
        for _, filename in config["images"].items():
            _, image = load.get_image(filename)
            zf.writestr(os.path.join("img", filename), image)

    memory_file.seek(0)

    return send_file(
        memory_file,
        download_name="who-is-who.zip",
        as_attachment=True,
        mimetype="application/zip",
    )
