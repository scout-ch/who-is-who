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


from . import extract, transform, load, renderer

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


@bp.route("/image/<string:person_id>", methods=["GET"])
def get_image(person_id):
    try:
        image = load.get_image(person_id)
        return Response(image["Body"].read(), mimetype=image["ContentType"])
    except Exception as e:
        return {"error": str(e)}, 404


@bp.route("/image-upload/<string:person_id>", methods=["POST"])
def image_upload(person_id):
    file = request.files["image"]
    load.upload_image(file, person_id)
    return "success"


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
            root_link="2",
            locale=locale,
            group_options=config["groups"],
            role_options=config["roles"],
            images=config["images"],
        )
        for key in group_pages:
            load.store(group_pages[key], str(key), builddir=f"api/static/{locale}")
            print(f"stored {len(groups_by_id)} files for locale {locale}")

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

    with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add files dynamically (could be from disk, database, etc.)
        for file in os.listdir("api/static"):
            zf.write(
                os.path.join("api/static", file),
                arcname=os.path.join("who-is-who", file),
            )

    memory_file.seek(0)

    return send_file(
        memory_file,
        download_name="who-is-who.zip",
        as_attachment=True,
        mimetype="application/zip",
    )
