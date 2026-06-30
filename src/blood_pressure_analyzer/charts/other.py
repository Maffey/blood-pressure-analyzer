from typing import Callable, TypeAlias

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from blood_pressure_analyzer.data_model import ColumnNames

StageClassifier: TypeAlias = Callable[[float], str]


def draw_weight_chart(df: pd.DataFrame) -> None:
    st.subheader("Weight in kilograms")
    st.line_chart(data=df, y=ColumnNames.WEIGHT)


def draw_category_histogram(df: pd.DataFrame) -> None:
    st.subheader("Blood category")
    chart_data = df[ColumnNames.CATEGORY].value_counts()
    st.bar_chart(chart_data, x_label="Blood category", y_label="Count")


_STAGE_COLORS = {
    "Normal": "seagreen",
    "Elevated": "goldenrod",
    "Stage 1 Hypertension": "darkorange",
    "Stage 2 Hypertension": "firebrick",
    "Hypertensive Crisis": "darkred",
}

_SYSTOLIC_STAGE_ORDER = [
    "Normal",
    "Elevated",
    "Stage 1 Hypertension",
    "Stage 2 Hypertension",
    "Hypertensive Crisis",
]

_DIASTOLIC_STAGE_ORDER = [
    "Normal",
    "Stage 1 Hypertension",
    "Stage 2 Hypertension",
    "Hypertensive Crisis",
]


def _classify_systolic_stage(value: float) -> str:
    if value < 120:
        return "Normal"
    if value < 130:
        return "Elevated"
    if value < 140:
        return "Stage 1 Hypertension"
    if value < 180:
        return "Stage 2 Hypertension"
    return "Hypertensive Crisis"


def _classify_diastolic_stage(value: float) -> str:
    if value < 80:
        return "Normal"
    if value < 90:
        return "Stage 1 Hypertension"
    if value < 120:
        return "Stage 2 Hypertension"
    return "Hypertensive Crisis"


def _stage_counts(
    df: pd.DataFrame,
    value_column: ColumnNames,
    stage_classifier: StageClassifier,
    stage_order: list[str],
) -> pd.Series:
    stages = df[value_column].dropna().map(stage_classifier).value_counts()
    return stages.reindex(stage_order).dropna()


def _draw_stage_pie_chart(
    df: pd.DataFrame,
    value_column: ColumnNames,
    stage_classifier: StageClassifier,
    title: str,
    stage_order: list[str],
) -> None:
    stages = _stage_counts(df, value_column, stage_classifier, stage_order)

    if stages.empty:
        st.info(f"No {title.lower()} data available for the selected date range.")
        return

    colors = [_STAGE_COLORS[label] for label in stages.index]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=stages.index,
                values=stages.values,
                hole=0.35,
                sort=False,
                marker=dict(colors=colors),
                textinfo="label+percent",
                hovertemplate="%{label}<br>Count: %{value}<br>Share: %{percent}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title=title,
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(orientation="v"),
    )

    st.plotly_chart(fig, width="stretch")


def draw_blood_pressure_stage_pies(df: pd.DataFrame) -> None:
    st.subheader("Most Common Blood Pressure Stages")
    st.caption(
        "Each chart classifies readings independently for systolic and diastolic values."
    )

    col1, col2 = st.columns(2)
    with col1:
        _draw_stage_pie_chart(
            df=df,
            value_column=ColumnNames.SYSTOLIC,
            stage_classifier=_classify_systolic_stage,
            title="Systolic Stage Distribution",
            stage_order=_SYSTOLIC_STAGE_ORDER,
        )
    with col2:
        _draw_stage_pie_chart(
            df=df,
            value_column=ColumnNames.DIASTOLIC,
            stage_classifier=_classify_diastolic_stage,
            title="Diastolic Stage Distribution",
            stage_order=_DIASTOLIC_STAGE_ORDER,
        )
