import logging
import os
import sys

from dotenv import load_dotenv
from IPython.display import display

from file_reader import read
from analyzer import changes_in_core_activities, changes_by_grouping, changes_for_region

logger: logging.Logger


def configure_logging():
    global logger
    logFormatter = "%(asctime)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        format=logFormatter,
        level=(os.environ.get("SRP_LOG_LEVEL") or "WARNING"),
    )

    logger = logging.getLogger(__name__)


def main():
    load_dotenv()
    configure_logging()

    logger.info("Starting SRF File Processor")

    logger.info("Read cluster growth profiles")
    file: str = os.environ.get("SRP_CGP_FILE", sys.argv[1])

    if file == "":
        logger.error("Must specify an input file in environment variable `SRP_CGP_FILE`")
        sys.exit(-1)

    df = read(file)
    # print(df.head())

    logger.info("Analyzing data")
    change_sc = changes_in_core_activities(df)
    display(change_sc)

    #group_changes = changes_by_grouping(change_sc)
    region_changes = changes_for_region(change_sc)

    display(region_changes)

    logger.info("Finished with file processing.")


if __name__ == "__main__":
    main()
