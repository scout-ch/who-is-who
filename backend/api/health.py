import datetime
from zoneinfo import ZoneInfo
import os


HEALTH_FOLDER = 'data/health'
DATA_LOAD_FILE = '/'.join([HEALTH_FOLDER, 'dataload'])
DATA_TRANSFORM_RESULT_FILE ='/'.join([HEALTH_FOLDER, 'data_transformation_result'])
LAST_LOGIN_FILE = '/'.join([HEALTH_FOLDER, 'last_login'])

def healthcheck():
    last_data_load = _last_data_load()
    last_data_transformation = _data_transformation_result()
    last_login = _last_login()

    if last_data_load == "" or last_data_transformation == "" or last_login == "":
        return {
            "status": "unready"
        }, 200

    last_updated = datetime.datetime.fromisoformat(last_data_load)
    degraded = (datetime.timedelta(hours=48) < datetime.datetime.now(ZoneInfo("Europe/Zurich")) - last_updated 
        or last_data_transformation == "failed")
    unhealthy = last_login == "failed"

    http_status = 503 if unhealthy else 200

    status = "unhealthy" if unhealthy else "degraded" if degraded else "healthy"

    return {
        "status": status,
        "checks": [
            _write_check("Last Data Load", last_data_load),
            _write_check("Data Transformation", last_data_transformation),
            _write_check("Last Login", last_login)
        ]
    }, http_status

def write_data_load_timestamp() -> None:
    _write_status(DATA_LOAD_FILE, datetime.datetime.now(ZoneInfo("Europe/Zurich")).replace(microsecond=0).isoformat())

def write_data_transformation_result(status: str) -> None:
    _write_status(DATA_TRANSFORM_RESULT_FILE, status)

def write_last_login_result(status: str) -> None:
    _write_status(LAST_LOGIN_FILE, status)

def _write_status(path: str, status: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write(status)

def _read_status(path) -> str:
    if not os.path.isfile(path):
        return ""

    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def _write_check(name: str, status: str) -> dict:
    return {
        "name": name,
        "status": status
    }
def _last_data_load():
    return _read_status(DATA_LOAD_FILE)

def _data_transformation_result():
    return _read_status(DATA_TRANSFORM_RESULT_FILE)

def _last_login():
    return _read_status(LAST_LOGIN_FILE)

