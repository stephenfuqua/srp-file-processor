import pandas as pd


def _get_change(df: pd.DataFrame, start_index: int, end_index: int, book: str) -> pd.Series:
    return df.loc[end_index, book] - df.loc[start_index, book]


def change_in_study_circle_participation(df: pd.DataFrame) -> pd.DataFrame:

    changes = pd.DataFrame(index=df["cluster_name"].unique())
    changes["completed_book_1"] = None
    changes["completed_book_2"] = None
    changes["completed_book_3_1"] = None
    changes["completed_book_3_2"] = None
    changes["completed_book_3_3"] = None
    changes["completed_book_4"] = None
    changes["completed_book_5"] = None
    changes["completed_book_6"] = None
    changes["completed_book_7"] = None
    changes["completed_book_8_1"] = None
    changes["completed_book_8_2"] = None
    changes["completed_book_8_3"] = None
    changes["completed_book_9_1"] = None
    changes["completed_book_9_2"] = None
    changes["completed_book_9_3"] = None
    changes["completed_book_10_1"] = None
    changes["completed_book_10_2"] = None
    changes["completed_book_10_3"] = None

    for cluster in changes.index:
        grouped = df[df["cluster_name"] == cluster]
        index = grouped.index

        end_index = index.max()

        if grouped.shape[0] > 2:
            start_index = end_index - 2

            for c in changes.columns:
                changes.loc[cluster, c] = _get_change(df, start_index, end_index, c)

    return changes
