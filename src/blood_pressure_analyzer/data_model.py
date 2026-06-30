from __future__ import annotations

from enum import StrEnum

from pandera import pandas as pa


class ColumnNames(StrEnum):
    DATE = "Date"
    SYSTOLIC = "Systolic"
    DIASTOLIC = "Diastolic"
    PULSE = "Pulse"
    IRREGULAR_HEARTBEAT = "Irregular heartbeat"
    CUFF_LOCATION = "Cuff location"
    BODY_POSITION = "Body position"
    WEIGHT = "Weight (kg)"
    NOTE = "Note"
    PULSE_PRESSURE = "Pulse pressure"
    MEAN_ARTERIAL_PRESSURE = "Mean arterial pressure"
    CATEGORY = "Category"


BLOOD_PRESSURE_SCHEMA = pa.DataFrameSchema(
    {
        ColumnNames.SYSTOLIC: pa.Column(float, nullable=False, coerce=True),
        ColumnNames.DIASTOLIC: pa.Column(float, nullable=False, coerce=True),
        ColumnNames.PULSE: pa.Column(float, nullable=True, coerce=True),
        ColumnNames.IRREGULAR_HEARTBEAT: pa.Column(
            str,
            nullable=False,
            coerce=True,
            checks=pa.Check.isin(["Yes", "No"]),
        ),
        ColumnNames.CUFF_LOCATION: pa.Column(str, nullable=False, coerce=True),
        ColumnNames.BODY_POSITION: pa.Column(str, nullable=False, coerce=True),
        ColumnNames.WEIGHT: pa.Column(float, nullable=True, coerce=True),
        ColumnNames.NOTE: pa.Column(str, nullable=True, coerce=True),
        ColumnNames.PULSE_PRESSURE: pa.Column(float, nullable=False, coerce=True),
        ColumnNames.MEAN_ARTERIAL_PRESSURE: pa.Column(
            float, nullable=False, coerce=True
        ),
        ColumnNames.CATEGORY: pa.Column(str, nullable=False, coerce=True),
    },
    index=pa.Index(pa.DateTime, name=ColumnNames.DATE, coerce=True),
    coerce=True,
    strict=False,
)
