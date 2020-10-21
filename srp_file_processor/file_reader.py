import re

import pandas as pd
import xlrd3 as xlrd

import constants


def _read_workbook(file: str) -> pd.DataFrame:
    book = xlrd.open_workbook(file)
    sheet = book.sheet_by_name("All Cycles")

    # Note that the SRP excel spreadsheets have a two-row header on them. Instead
    # of trying to read the headers, we will hard-code the header values and skip
    # the first two rows.
    cycle_data = list()
    for i in range(3, sheet.nrows):
        in_row = sheet.row(i)

        out_row = list()
        cycle_data.append(out_row)

        for j in range(sheet.ncols):
            out_row.append(in_row[j].value)

    df = pd.DataFrame(cycle_data)
    df.columns = constants.CGP_HEADERS

    return df


def _extract_cluster_name(df: pd.DataFrame) -> pd.DataFrame:
    expression = re.compile(r"[A-Za-z0-9\-]+ (.+)$")

    def _get_name(x):
        m = expression.match(x)
        if m:
            return m.group(1)

        return None

    df[constants.CLUSTER_NAME] = df["cluster"].apply(_get_name)

    return df


def _add_grouping(df: pd.DataFrame) -> pd.DataFrame:
    def _get_grouping(x):
        return constants.GROUPINGS.get(x, None)

    df[constants.GROUPING] = df["cluster_name"].apply(_get_grouping)

    return df


def read(file):
    df = _read_workbook(file)
    df = _extract_cluster_name(df)
    df = _add_grouping(df)

    return df
