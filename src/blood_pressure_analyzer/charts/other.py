import pandas as pd
import streamlit as st

from blood_pressure_analyzer.data_model import ColumnNames


def draw_weight_chart(df: pd.DataFrame) -> None:
    st.subheader("Weight in kilograms")
    st.line_chart(data=df, y=ColumnNames.WEIGHT)


def draw_category_histogram(df: pd.DataFrame) -> None:
    st.subheader("Blood category")
    chart_data = df[ColumnNames.CATEGORY].value_counts()
    st.bar_chart(chart_data, x_label="Blood category", y_label="Count")
