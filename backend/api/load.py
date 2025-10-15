import json
import os
import logging

from api.app import APPNAME

from openstack import connection

log = logging.getLogger(".".join((APPNAME, "Load")))

container_name = os.environ["SWIFT_CONTAINER"]

conn = connection.Connection(
    region_name=os.environ["SWIFT_REGION"],
    auth_url=os.environ["SWIFT_AUTH_URL"],
    project_name=os.environ["SWIFT_PROJECT"],
    username=os.environ["SWIFT_USERNAME"],
    password=os.environ["SWIFT_PASSWORD"],
    user_domain_name="Default",
    project_domain_name="Default",
)


def ensure_container(name):
    try:
        for cont in conn.object_store.containers():
            if cont.name == name:
                return cont
    except Exception as e:
        log.error(f"Error fetching container: {e}")
        return None
    finally:
        log.info(f"Container {name} not found, creating new")
        return conn.object_store.create_container(name=name)


ensure_container(container_name)


def upload_html(group_id, locale, page):
    filename = f"g_{group_id}_{locale}.html"
    _upload_object(name=filename, data=page.encode("utf-8"), content_type="text/html")


def upload_image(image, imagename):
    filename = imagename + os.path.splitext(image.filename)[1]
    _upload_object(name=filename, data=image, content_type=image.content_type)
    return filename


def _upload_object(name, data, content_type):
    try:
        conn.object_store.upload_object(
            container=container_name,
            name=name,
            data=data,
            content_type=content_type,
        )
    except Exception as e:
        log.error(f"Upload failed: {e}")


def get_image(imagename):
    obj = next(conn.object_store.objects(container=container_name, prefix=imagename))
    return obj, conn.object_store.download_object(obj=obj)


def get_html(group_id, locale):
    filename = f"g_{group_id}_{locale}.html"
    return conn.object_store.download_object(container=container_name, obj=filename)


def store(page, page_name, builddir="build"):
    filename = os.path.join(builddir, _filename(page_name, "html"))

    if not os.path.exists(builddir):
        os.makedirs(builddir)

    report = "replaced" if os.path.exists(filename) else "created"

    with open(filename, mode="w", encoding="utf-8") as f:
        f.write(page)
        print(f"-- {report} {filename}")


def _filename(path, extension="html"):
    if path.split(".")[-1] != extension:
        path = ".".join([path, extension])
    return path


def store_to_json(data, filepath="transformed_data.json"):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
        )


def read_json(file):
    if not os.path.isfile(file):
        return {}

    with open(file, "r", encoding="utf-8") as file:
        return json.load(file)
