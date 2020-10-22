import pandas as pd

import constants


def _get_change(
    df: pd.DataFrame, start_index: int, end_index: int, book: str
) -> pd.Series:
    return df.loc[end_index, book] - df.loc[start_index, book]


def change_in_study_circle_participation(df: pd.DataFrame) -> pd.DataFrame:

    changes = pd.DataFrame(index=df["cluster_name"].unique())
    changes["grouping"] = None
    changes["cluster_name"] = changes.index

    for c in constants.STUDY_CIRCLE_PARTICIPATION_COLUMNS:
        changes[c] = None

    for cluster in changes.index:
        grouped = df[df["cluster_name"] == cluster]
        index = grouped.index

        end_index = index.max()

        if grouped.shape[0] > 2:
            start_index = end_index - 2

            changes["grouping"] = df.loc[start_index, "grouping"]

            for c in constants.STUDY_CIRCLE_PARTICIPATION_COLUMNS:
                changes.loc[cluster, c] = _get_change(df, start_index, end_index, c)
        else:
            # Only interested in the clusters with multiple cycles
            changes.drop(cluster, inplace=True)

    return changes
