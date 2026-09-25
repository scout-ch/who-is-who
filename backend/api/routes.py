import logging

from flask import Blueprint, Response, jsonify, request

from api import configuration, data, renderer
from api.app import APPNAME
from api.data import ROOT_GROUP
from api.health import healthcheck
from api.services.storage import get_storage_service

log = logging.getLogger(".".join((APPNAME, "Renderer")))

bp = Blueprint("/", __name__)


@bp.route("/", methods=["GET"])
def index():
    return jsonify(data.get())


@bp.route("/health", methods=["GET"])
def get_health():
    return healthcheck()


@bp.route("/full_html/<string:locale>/<int:group_id>", methods=["GET"])
def get_full_html(locale, group_id):
    name = f"api/html/{locale}/{group_id}"
    obj = get_storage_service().get_object(name=name)
    if not obj:
        return "no such file", 404

    html = get_storage_service().download_file(obj)
    return "".join((renderer.html_start(), html.decode(), renderer.html_end()))


@bp.route("/image/<string:person_id>", methods=["GET", "POST"])
def get_image(person_id):
    name = f"img/{person_id}"
    if request.method == "POST":
        file = request.files["image"]
        get_storage_service().upload_file(
            name=name, data=file, content_type=file.content_type
        )
        return {"filename": name}
    obj = get_storage_service().get_object(name=name)
    if not obj:
        return "no such file", 404

    image = get_storage_service().download_file(obj)
    return Response(image, mimetype=obj.content_type)


@bp.route("/fetch-data", methods=["GET"])
def fetch_data():
    return data.try_load()


@bp.route("/render", methods=["GET"])
def render():
    for locale in ["de", "fr", "it"]:
        html = renderer.render_group(
            locale=locale,
            root_id=str(ROOT_GROUP),
        )
        name = f"api/html/{locale}/{ROOT_GROUP}"
        get_storage_service().upload_file(
            name=name, data=html.encode("utf-8"), content_type="text/html"
        )
        log.info(f"uploaded file ${name}")
    return Response(status=200)


@bp.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        configuration.set_config(request.get_json()["data"])
        return Response(status=200)
    elif request.method == "GET":
        return jsonify(configuration.get())
    return Response(status=400)
