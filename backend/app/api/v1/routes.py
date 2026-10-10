import logging

from flask import Blueprint, Response, jsonify, request

from app.core.codes import APPNAME, ROOT_GROUP
from app.core.config import OBJECT_STORAGE_URL
from app.services.configuration import configuration
from app.services.data import data
from app.services.generator import renderer
from app.services.health.health import healthcheck
from app.services.storage import get_storage_service

log = logging.getLogger(".".join((APPNAME, "Renderer")))

bp = Blueprint("/", __name__)


@bp.route("/", methods=["GET"])
def index():
    return jsonify(data.get())


@bp.route("/health", methods=["GET"])
def get_health():
    return healthcheck()


@bp.route("/render", methods=["GET"])
def render():
    for locale in ["de", "fr", "it"]:
        log.info(f"Rendering locale {locale}")
        html = renderer.render_group(
            locale=locale,
            root_id=str(ROOT_GROUP),
        )

        name = f"api/html/{locale}/{ROOT_GROUP}"

        log.info(f"Uploading to {name}")
        get_storage_service().upload_file(
            name=name, data=html.encode("utf-8"), content_type="text/html"
        )
        log.info(f"uploaded file {name}")
    return Response(status=200)


@bp.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        configuration.set_config(request.get_json()["data"])
        return Response(status=200)
    elif request.method == "GET":
        return jsonify(configuration.get())
    return Response(status=400)


@bp.route("/object_storage", methods=["GET"])
def object_storage():
    return {"url": OBJECT_STORAGE_URL}, 200
