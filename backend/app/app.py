import logging
import sys

from flask import Flask
from flask_cors import CORS

from app.services.storage import init_storage

logger = logging.getLogger(__name__)


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

    from app.api.v1 import routes

    app.register_blueprint(routes.bp)

    return app
