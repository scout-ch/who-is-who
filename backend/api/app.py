import logging
import sys

from flask import Flask
from flask_cors import CORS

from api.services.storage import init_storage

logger = logging.getLogger(__name__)

APPNAME = "WIW_API"


def create_app():
    # Start logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        stream=sys.stdout,
    )

    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    init_storage(app)

    from . import routes

    app.register_blueprint(routes.bp)

    return app
