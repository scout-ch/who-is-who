import logging
import os
import zipfile
from io import BytesIO

from flask import Blueprint, Response, jsonify, redirect, request, send_file

from api import configuration, data, load, renderer
from api.app import APPNAME

log = logging.getLogger(".".join((APPNAME, "Renderer")))

bp = Blueprint("/", __name__)


ROOT_GROUP = str(
    os.environ.get("ROOT_GROUP") if os.environ.get("ROOT_GROUP") else "0"
)  # PBS Midata Group ID


@bp.route("/", methods=["GET"])
def index():
    return jsonify(data.get(ROOT_GROUP))


@bp.route("/full_html/<string:locale>/<int:group_id>", methods=["GET"])
def get_full_html(locale, group_id):
    try:
        html = load.get_html(group_id, locale)
        return "".join((renderer.html_start(), html.decode(), renderer.html_end()))
    except Exception as e:
        return {"error": str(e)}, 404


@bp.route("/html/<string:locale>/<int:group_id>", methods=["GET"])
def get_html(locale, group_id):
    try:
        html = load.get_html(group_id, locale)
        return html.decode()
    except Exception as e:
        return {"error": str(e)}, 404


@bp.route("/<path:_prefix>/styles.css", methods=["GET"])
def get_style(_prefix):
    return send_file("styles.css")


@bp.route("/image/<string:person_id>", methods=["GET", "POST"])
def get_image(person_id):
    if request.method == "POST":
        file = request.files["image"]
        filename = load.upload_image(file, person_id)
        return {"filename": filename}
    try:
        obj, image = load.get_image(person_id)
        return Response(image, mimetype=obj.content_type)
    except Exception as e:
        return {"error": str(e)}, 404


@bp.route("/api/static/<path:p>")
def get_static(p):
    return redirect(f"/static/{p}")


@bp.route("/fetch-data", methods=["GET"])
def fetch_data():
    data.fetch_and_store(ROOT_GROUP)
    return Response(status=200)


@bp.route("/render", methods=["GET"])
def render():
    for locale in ["de", "fr", "it"]:
        page = renderer.render_group(
            locale=locale,
            root_id=str(ROOT_GROUP),
        )
        load.upload_html(str(ROOT_GROUP), locale, page)

    return Response(status=200)


@bp.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        configuration.set_config(request.get_json()["data"])
        return Response(status=200)
    elif request.method == "GET":
        return jsonify(configuration.get())
    return Response(status=400)


@bp.route("/download-zip")
def download_zip():
    memory_file = BytesIO()

    group_id = str(ROOT_GROUP)
    pages = {}
    locales = ["de", "fr", "it"]
    pages = {
        "_".join((group_id, locale + ".html")): load.get_html(group_id, locale)
        for locale in locales
    }

    with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add html pages
        for filename, html in pages.items():
            zf.writestr(filename, html)
        # Add styles.css
        zf.write("api/styles.css", "styles.css")
        # Add images
        zf.write("api/static/favicon.png", "img/logo.png")
        for filename in configuration.images():
            _, image = load.get_image(filename)
            zf.writestr(os.path.join("img", filename), image)

    memory_file.seek(0)

    return send_file(
        memory_file,
        download_name="who-is-who.zip",
        as_attachment=True,
        mimetype="application/zip",
    )
