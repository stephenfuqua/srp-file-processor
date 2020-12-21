import logging
import os
import sys

from dotenv import load_dotenv
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

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

    logger.info("Starting SRF Analysis Dashboard")

    logger.info("Reading cluster growth profiles")
    file: str = os.environ.get("SRP_CGP_FILE", os.sys.argv[1])

    if file == "":
        logger.error(
            "Must specify an input file in environment variable `SRP_CGP_FILE`"
        )
        sys.exit(-1)

    df = read(file)

    logger.info("Analyzing data")
    change_cluster = changes_in_core_activities(df)
    changes_region = changes_for_region(change_cluster)

    logger.info("Finished with file processing.")

    logger.info("Starting dashboard")

    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    fig = px.bar(
        changes_region.transpose(),
        orientation="h",
        title="South Central Region",
        labels={"value": "", "variable": ""},
    )

    app.layout = html.Div(
        children=[
            html.H1(children="SRP Analysis Dashboard"),
            html.H2(children="Changes Over Past Two Cycles"),
            dcc.Graph(id="example-graph", figure=fig),
        ]
    )

    app.run_server(debug=True)


if __name__ == "__main__":
    main()
