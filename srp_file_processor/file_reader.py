import re
from typing import List

import pandas as pd
import xlrd3 as xlrd

import constants


def _read_workbook(file: str, sheet_name: str, num_header_rows: int, columns: List[str]) -> pd.DataFrame:
    book = xlrd.open_workbook(file)
    sheet = book.sheet_by_name(sheet_name)

    # Note that the SRP excel spreadsheets have a multi-row header on them. Instead
    # of trying to read the headers, we will hard-code the header values and skip
    # the first n rows.
    cycle_data = list()
    for i in range(num_header_rows + 1, sheet.nrows):
        in_row = sheet.row(i)

        out_row = list()
        cycle_data.append(out_row)

        for j in range(sheet.ncols):
            out_row.append(in_row[j].value)

    df = pd.DataFrame(cycle_data)
    df.columns = columns

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


def read_cgp(file):
    df = _read_workbook(file, "All Cycles", 2, constants.CGP_HEADERS)
    df = _normalize_cluster_name(df)
    df = _add_grouping(df)

    return df


def read_activities(file):
    df = _read_workbook(file, "All Activities", 2, constants.ACTIVITIES_HEADER)
    df = _normalize_cluster_name(df)
    df = _add_grouping(df)

    return df
