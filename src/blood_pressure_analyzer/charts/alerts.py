import pandas as pd
import streamlit as st


def show_irregular_heartbeat_alert(df: pd.DataFrame):
    if df.empty or "Irregular heartbeat" not in df.columns:
        return

    latest_date = df.index.max()
    date_14_days_ago = latest_date - pd.Timedelta(days=14)

    recent_14_df = df[df.index > date_14_days_ago]

    irregular_readings = recent_14_df[recent_14_df["Irregular heartbeat"] == "Yes"]

    if not irregular_readings.empty:
        count = len(irregular_readings)
        most_recent = irregular_readings.index.max().strftime("%Y-%m-%d %H:%M")

        st.error(
            f"⚠️ **Irregular Heartbeat Detected!** \n\n"
            f"You logged **{count}** reading(s) with an irregular heartbeat in the last 14 days. "
            f"*(Most recent: {most_recent})*"
        )
    else:
        st.success("❤️ No irregular heartbeats detected in the last 14 days.")
