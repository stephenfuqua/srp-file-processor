import logging
import os
import sys

from dotenv import load_dotenv

from file_reader import read
from analyzer import change_in_study_circle_participation

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
    file: str = os.environ.get("SRP_CGP_FILE", "")

    if file == "":
        logger.error("Must specify an input file in environment variable `SRP_CGP_FILE`")
        sys.exit(-1)

    df = read(file)
    print(df.head())

    logger.info("Analyzing data")
    change_sc = change_in_study_circle_participation(df)
    print(change_sc.head())

    logger.info("Finished with file processing.")


if __name__ == "__main__":
    main()
