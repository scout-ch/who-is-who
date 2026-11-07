import logging
import sys

from app.services.etl.etl import run_etl

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        stream=sys.stdout,
    )

    log = logging.getLogger("Update Data")

    log.info("======= Start update =======")
    run_etl()
    log.info("=======  End update  =======")
