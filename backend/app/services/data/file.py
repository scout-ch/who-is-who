import json
import logging
import os

from app.core.codes import APPNAME

log = logging.getLogger(".".join((APPNAME, "JSON Interface")))


def store(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
        )


def read(file):
    if not os.path.isfile(file):
        return {}

    with open(file, "r", encoding="utf-8") as file:
        return json.load(file)
