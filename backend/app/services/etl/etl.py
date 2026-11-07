import logging

from app.core.codes import (
    APPNAME,
    DATA_FILE,
    GROUPS_LABEL,
    IMAGE_LABEL,
    ROLES_BY_GROUPS_LABEL,
    ROLES_LABEL,
    ROOT_GROUP,
    SUBGROUPS_LABEL,
)
from app.services.data import file
from app.services.health.health import (
    write_data_load_timestamp,
    write_data_transformation_result,
    write_last_login_result,
)

from . import extract, transform

log = logging.getLogger(".".join((APPNAME, "ETL")))


def run_etl():
    try:
        try_load()
    except ConnectionError as ce:
        write_last_login_result("failed")
        log.error(str(ce))
        return ["error"], 500
    except RuntimeError as re:
        write_data_transformation_result("failed")
        log.error(str(re))
        return ["error"], 500
    except Exception as e:
        log.error(str(e))
        return ["error"], 500

    write_data_transformation_result("successful")
    write_last_login_result("successful")
    write_data_load_timestamp()


def try_load():
    log.info("Loading organsiation data")
    groups, roles, people = extract.api_fetch_organisation_data(ROOT_GROUP)

    log.info("Transforming data")
    groups_by_id, subgroups_for_groups, roles_by_id, roles_for_groups, images = (
        transform.t(groups, roles, people)
    )
    transformed_data = {
        GROUPS_LABEL: groups_by_id,
        SUBGROUPS_LABEL: subgroups_for_groups,
        ROLES_LABEL: roles_by_id,
        ROLES_BY_GROUPS_LABEL: roles_for_groups,
        IMAGE_LABEL: images,
    }

    log.info("Storing data")
    file.store(transformed_data, DATA_FILE)

    log.info("Finished data update")
