
from pathlib import Path
import pandas as pd

def parse_blood_pressure_csv(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path, parse_dates=True)
    return df