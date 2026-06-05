import streamlit as st

from blood_pressure_analyzer.charts.blood_pressure import draw_blood_pressure_chart
from blood_pressure_analyzer.charts.other import (
    draw_weight_chart,
    draw_category_histogram,
)
from blood_pressure_analyzer.csv_parser import (
    parse_blood_pressure_csv,
    get_time_range,
    TimeRange,
)

_PAGE_TITLE = "Blood Pressure Analyzer"

# TODO LIST
# TODO prek, ruff
# TODO average line
# TODO hwo to display multiple record per day?
# TODO in diagram ,where normal occurrences?
# TODO pie-chart of what I end up mostly with (what blood pressure stage)
# TODO other data to be displayed, and other type of charts
# TODO use pandera, maybe pydantic as well
# TODO docker?
# TODO hosting?


def main():
    st.title(_PAGE_TITLE)
    st.set_page_config(
        page_title=_PAGE_TITLE,
        page_icon="static/images/droplet_solid.svg",
        layout="wide",
    )

    blood_pressure_data = st.file_uploader(
        "Choose a CSV file exported from BP Journal:", type="csv"
    )
    if blood_pressure_data is None:
        return

    bp_df = parse_blood_pressure_csv(blood_pressure_data)
    with st.expander("Table View of Data Source"):
        st.dataframe(bp_df)
    time_range = get_time_range(bp_df)

    selected_time_range = TimeRange(
        *st.slider(
            "Date range",
            min_value=time_range.start,
            max_value=time_range.end,
            value=time_range,
        )
    )

    filtered_bp_df = bp_df[selected_time_range.start : selected_time_range.end]

    draw_blood_pressure_chart(filtered_bp_df)
    draw_category_histogram(filtered_bp_df)
    draw_weight_chart(filtered_bp_df)


if __name__ == "__main__":
    main()
