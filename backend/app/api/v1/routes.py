import logging

from flask import Blueprint, Response, jsonify, request

from app.core.codes import APPNAME, PREVIEW_FILE, ROOT_GROUP
from app.core.config import LOCALES, OBJECT_STORAGE_URL
from app.services.configuration import configuration
from app.services.data import data, file
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
    log.info(f"Rendering locales {LOCALES}")
    previews = {
        locale: renderer.render_group(
            locale=locale,
            root_id=str(ROOT_GROUP),
        )
        for locale in LOCALES
    }
    file.store(previews, PREVIEW_FILE)
    log.info("Stored previews")

    return previews, 200


@bp.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        configuration.set_config(request.get_json()["data"])
        return Response(status=200)
    elif request.method == "GET":
        return jsonify(configuration.get())
    return Response(status=400)


@bp.route("/preview", methods=["GET"])
def preview():
    return file.read(PREVIEW_FILE)


@bp.route("/publish", methods=["GET"])
def publish():
    previews = file.read(PREVIEW_FILE)
    for locale in LOCALES:
        name = f"api/html/{locale}/{ROOT_GROUP}"
        log.info(f"Uploading to {name}")
        get_storage_service().upload_file(
            name=name, data=previews[locale].encode("utf-8"), content_type="text/html"
        )
        log.info(f"uploaded file {name}")
    return {"url": OBJECT_STORAGE_URL}, 200
