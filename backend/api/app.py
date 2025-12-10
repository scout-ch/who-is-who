import os

from flask import Flask
from flask_cors import CORS

APPNAME = "WIW_API"


def create_app():
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    from . import routes

    app.register_blueprint(routes.bp)

    return app
