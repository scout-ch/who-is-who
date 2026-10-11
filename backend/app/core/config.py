import os

OBJECT_STORAGE_URL = os.environ["OS_URL"]
CONTAINER_NAME = os.environ["SWIFT_CONTAINER"]

TOKEN = os.environ.get("HITOBITO_TOKEN")
URL = os.environ.get("HITOBITO_URL")
LOCALES = ["de", "fr", "it"]
