import pandas as pd

import constants


def _get_change(
    df: pd.DataFrame, start_index: int, end_index: int, book: str
) -> pd.Series:
    return df.loc[end_index, book] - df.loc[start_index, book]


def changes_in_core_activities(profiles: pd.DataFrame) -> pd.DataFrame:

    changes = pd.DataFrame(index=profiles["cluster_name"].unique())
    changes[constants.GROUPING] = None
    changes[constants.CLUSTER_NAME] = changes.index

    for c in constants.ANALYZE_PARTICIPATION_COLUMNS:
        changes[c] = None

    for cluster in changes.index:
        grouped = profiles[profiles["cluster_name"] == cluster]
        index = grouped.index

        end_index = index.max()

        if grouped.shape[0] > 2:
            start_index = end_index - 2

            changes.loc[cluster, "grouping"] = profiles.loc[start_index, "grouping"]

            for c in constants.ANALYZE_PARTICIPATION_COLUMNS:
                changes.loc[cluster, c] = _get_change(profiles, start_index, end_index, c)
        else:
            # Only interested in the clusters with multiple cycles
            changes.drop(cluster, inplace=True)

    return changes


def changes_by_grouping(changes: pd.DataFrame):  # -> pd.DataFrame:
    groups = changes.groupby(by=[constants.GROUPING])
    group_changes = groups.sum().copy()
    group_changes.drop(columns=["cluster_name"])

    return group_changes


def changes_for_region(changes: pd.DataFrame) -> pd.Series:
    region_changes = changes.sum()

    return region_changes
