from flask import current_app

from .client import ObjectStorageService, get_openstack_connection


def init_storage(app):
    app.extensions["storage"] = ObjectStorageService(get_openstack_connection())


def get_storage_service() -> ObjectStorageService:
    return current_app.extensions["storage"]  # type: ignore[no-any-return]
