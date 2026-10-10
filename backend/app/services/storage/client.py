import logging
import os

import openstack
import requests.exceptions
from openstack.connection import Connection
from openstack.object_store.v1.obj import Object
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

log = logging.getLogger("Object Storage Client")

container_name = os.environ["SWIFT_CONTAINER"]


def get_openstack_connection() -> Connection:
    return openstack.connect()


class ObjectStorageService:
    def __init__(self, connection):
        self._container_name = container_name
        self._conn: Connection = connection
        self._check_container()

    def _check_container(self):
        containers = list(
            self._conn.object_store.containers(name=self._container_name, limit=2)
        )

        if len(containers) == 0:
            log.warning(
                f"No container named '${self._container_name}' in object store: creating container"
            )
            return self._conn.object_store.create_container(name=self._container_name)
        if len(containers) == 1:
            return containers[0]

        container_names = "\n".join([container.name for container in containers])
        warning_string = (
            f"Container name '${self._container_name}' ambigous: \n${container_names}"
        )
        log.warning(warning_string)
        raise RuntimeError(warning_string)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, max=4),
        retry=retry_if_exception_type(
            (requests.exceptions.ConnectionError, requests.exceptions.Timeout)
        ),
    )
    def upload_file(self, name: str, data, content_type) -> Object | None:
        return self._conn.object_store.upload_object(
            container=self._container_name,
            name=name,
            data=data,
            content_type=content_type,
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, max=4),
        retry=retry_if_exception_type(
            (requests.exceptions.ConnectionError, requests.exceptions.Timeout)
        ),
    )
    def get_object(
        self,
        name: str,
    ) -> Object | None:
        objs = list(
            self._conn.object_store.objects(container=container_name, name=name)
        )
        if len(objs) == 0:
            log.warning(f"No such object: ${name}")
            return None
        if len(objs) != 1:
            log.warning(f"multiple image present in object storage for name: ${name}")
        return objs.pop()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, max=4),
        retry=retry_if_exception_type(
            (requests.exceptions.ConnectionError, requests.exceptions.Timeout)
        ),
    )
    def download_file(self, obj: Object) -> bytes:
        return self._conn.object_store.download_object(obj)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, max=4),
        retry=retry_if_exception_type(
            (requests.exceptions.ConnectionError, requests.exceptions.Timeout)
        ),
    )
    def delete_file(self, obj: Object) -> None:
        self._conn.object_store.delete_object(obj)

    # def generate_presigned_url(self, container: str, object_name: str, expires_in: int = 3600) -> str:
