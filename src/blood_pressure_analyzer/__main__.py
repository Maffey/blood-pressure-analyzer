from pathlib import Path

import pandas as pd
import streamlit as st

from blood_pressure_analyzer.charts.other import draw_weight_chart, draw_category_histogram
from blood_pressure_analyzer.csv_parser import parse_blood_pressure_csv, get_time_range, TimeRange


def main():
    st.title("Blood Pressure Analyzer")
    bp_df = parse_blood_pressure_csv(Path("input_data/Mateusz_20250212_20260603.csv"))
    with st.expander("Table View of Data Source"):
        st.dataframe(bp_df)
    time_range = get_time_range(bp_df)

    selected_time_range = TimeRange(*st.slider("Date range",
              min_value=time_range.start,
              max_value=time_range.end,
              value=time_range))

    filtered_bp_df = bp_df[selected_time_range.start:selected_time_range.end]

    draw_weight_chart(filtered_bp_df)
    draw_category_histogram(filtered_bp_df)



if __name__ == "__main__":
    main()
