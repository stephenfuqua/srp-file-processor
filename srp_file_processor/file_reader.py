import re
from typing import List

import pandas as pd

import constants


def _read_workbook(file: str, sheet_name: str, num_header_rows: int, columns: List[str]) -> pd.DataFrame:
    df = pd.read_excel(
        file,
        sheet_name=sheet_name,
        skiprows=num_header_rows,
        engine='openpyxl'
    )

    df.columns = columns
    df.fillna(0, inplace=True)

    return df


def _normalize_cluster_name(df: pd.DataFrame) -> pd.DataFrame:
    expression = re.compile(r"[A-Za-z0-9\-]+ (.+)$")

    def _get_name(x):
        m = expression.match(x)
        if m:
            return m.group(1)

        return None

    df[constants.CLUSTER_NAME] = df[constants.CLUSTER].apply(_get_name)

    return df


def _add_grouping(df: pd.DataFrame) -> pd.DataFrame:
    def _get_grouping(x):
        return constants.GROUPINGS.get(x, None)

    df[constants.GROUPING] = df[constants.CLUSTER_NAME].apply(_get_grouping)

    return df


def read_cgp_all_cycles(file):
    df = _read_workbook(file, "All Cycles", 3, constants.CGP_HEADERS)
    df = _normalize_cluster_name(df)
    df = _add_grouping(df)

    return df


def read_cgp_latest(file):
    df = _read_workbook(file, "Latest Cycle", 2, constants.CGP_HEADERS)
    df = _normalize_cluster_name(df)
    df = _add_grouping(df)

    return df


def read_activities(file):
    df = _read_workbook(file, "All Activities", 2, constants.ACTIVITIES_HEADER)
    df = _normalize_cluster_name(df)
    df = _add_grouping(df)

    return df
