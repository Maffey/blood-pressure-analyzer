import pandas as pd
import streamlit as st


def show_metrics(df: pd.DataFrame):
    def render_metric(col, label, key):
        current_val = recent_avg[key]

        if not pd.isna(prev_avg[key]):
            delta_val = current_val - prev_avg[key]
            col.metric(
                label=label,
                value=f"{current_val:.1f}",
                delta=f"{delta_val:.1f}",
                delta_color="inverse",
            )
        else:
            col.metric(
                label=label,
                value=f"{current_val:.1f}",
                delta="Needs more data",
                delta_color="off",
            )

    latest_date = df.index.max()
    date_14_days_ago = latest_date - pd.Timedelta(days=14)
    date_28_days_ago = latest_date - pd.Timedelta(days=28)

    recent_14_df = df[df.index > date_14_days_ago]
    prev_14_df = df[(df.index <= date_14_days_ago) & (df.index > date_28_days_ago)]

    recent_avg = recent_14_df[
        ["Systolic", "Diastolic", "Pulse", "Mean arterial pressure"]
    ].mean()
    prev_avg = prev_14_df[
        ["Systolic", "Diastolic", "Pulse", "Mean arterial pressure"]
    ].mean()

    st.subheader("14-Day Average vs. Previous 14 Days Average")
    col1, col2, col3, col4 = st.columns(4)

    render_metric(col1, "Avg Systolic", "Systolic")
    render_metric(col2, "Avg Diastolic", "Diastolic")
    render_metric(col3, "Avg Pulse", "Pulse")
    render_metric(col4, "Avg MAP", "Mean arterial pressure")
