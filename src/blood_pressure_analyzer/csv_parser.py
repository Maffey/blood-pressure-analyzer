import datetime as dt
from pathlib import Path
from typing import NamedTuple

import pandas as pd

class TimeRange(NamedTuple):
    start: dt.datetime
    end: dt.datetime


def parse_blood_pressure_csv(csv_path: Path) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(csv_path, parse_dates=True, index_col=0)
    return df.sort_index()


def get_time_range(df: pd.DataFrame) -> TimeRange:
    return TimeRange(start=df.index.min().to_pydatetime(), end=df.index.max().to_pydatetime())