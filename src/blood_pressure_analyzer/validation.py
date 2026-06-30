from __future__ import annotations

import pandera.errors as pa_errors
import pandas as pd

from blood_pressure_analyzer.data_model import BLOOD_PRESSURE_SCHEMA


class BloodPressureCsvValidationError(ValueError):
    pass


def validate_blood_pressure_frame(df: pd.DataFrame) -> pd.DataFrame:
    try:
        return BLOOD_PRESSURE_SCHEMA.validate(df, lazy=True)
    except (pa_errors.SchemaError, pa_errors.SchemaErrors) as exc:
        raise BloodPressureCsvValidationError(
            "Uploaded CSV does not match the BP Journal export format."
        ) from exc
