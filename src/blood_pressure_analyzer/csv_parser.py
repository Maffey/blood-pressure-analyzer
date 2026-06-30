import datetime as dt
from typing import NamedTuple

import pandas as pd

from blood_pressure_analyzer.validation import validate_blood_pressure_frame


class TimeRange(NamedTuple):
    start: dt.datetime
    end: dt.datetime


def parse_blood_pressure_csv(csv_path: object) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(csv_path, parse_dates=[0], index_col=0)
    validated_df = validate_blood_pressure_frame(df)
    return validated_df.sort_index()


def get_time_range(df: pd.DataFrame) -> TimeRange:
    return TimeRange(
        start=df.index.min().to_pydatetime(), end=df.index.max().to_pydatetime()
    )
