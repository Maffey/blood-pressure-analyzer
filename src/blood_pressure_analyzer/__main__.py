import streamlit as st

from blood_pressure_analyzer.charts.alerts import show_irregular_heartbeat_alert
from blood_pressure_analyzer.charts.blood_pressure import draw_all_blood_pressure_charts
from blood_pressure_analyzer.charts.metrics import show_metrics
from blood_pressure_analyzer.charts.other import (
    draw_weight_chart,
    draw_category_histogram,
    draw_blood_pressure_stage_pies,
)
from blood_pressure_analyzer.csv_parser import (
    TimeRange,
    parse_blood_pressure_csv,
    get_time_range,
)
from blood_pressure_analyzer.validation import BloodPressureCsvValidationError

_PAGE_TITLE = "Blood Pressure Analyzer"
# TODO
# Done. Here's what changed.
# Dockerfile — config is now env-var driven so any host can override the port without a rebuild:
# •
# Added STREAMLIT_SERVER_ADDRESS=0.0.0.0, STREAMLIT_SERVER_PORT=8501, STREAMLIT_SERVER_HEADLESS=true.
# •
# Entrypoint slimmed to just streamlit run … (flags moved to env).
# •
# HEALTHCHECK now reads STREAMLIT_SERVER_PORT so it stays correct if the port is overridden.
# fly.toml (new) — ready to deploy:
# •
# internal_port = 8501, force_https, builds from the Dockerfile.
# •
# Scale-to-zero (auto_stop_machines = "stop", min_machines_running = 0) — free when idle.
# •
# Connection-based concurrency so Streamlit's long-lived WebSocket sessions don't get a machine reaped mid-use.
# •
# HTTP health check on /_stcore/health.
# •
# shared-cpu-1x / 512 MB VM (note in-file: bump to 1 GB if pandas OOMs).
# •
# primary_region = "waw" (Warsaw) — change if you're elsewhere.
# README.md — added a "Deploy to Fly.io" section (fly launch --no-deploy → fly deploy → fly open) and a note about overriding the port.
# .dockerignore — excluded fly.toml from the image context.
# __main__.py — removed the now-resolved # TODO hosting? block.
# To ship it:
# fly launch --no-deploy   # claim a unique app name/region (keeps this fly.toml)
# fly deploy
# fly open
# One thing to decide before it's public: the app is open to anyone with the URL. Each visitor uploads their own CSV (so no leak of your data, and nothing is persisted server-side), but if you'd rather lock it down, the simplest path on Fly is basic-auth via a tiny proxy or Fly's access controls — say the word and I'll wire it in.


def main():
    st.set_page_config(
        page_title=_PAGE_TITLE,
        page_icon="static/images/droplet_solid.svg",
        layout="wide",
    )
    st.title(_PAGE_TITLE)

    blood_pressure_data = st.file_uploader(
        "Choose a CSV file exported from BP Journal:", type="csv"
    )
    if blood_pressure_data is None:
        return

    try:
        bp_df = parse_blood_pressure_csv(blood_pressure_data)
    except BloodPressureCsvValidationError as exc:
        st.error(str(exc))
        st.stop()

    with st.expander("Table View of Data Source"):
        st.dataframe(bp_df)
    time_range = get_time_range(bp_df)

    show_metrics(bp_df)
    show_irregular_heartbeat_alert(bp_df)

    selected_time_range = TimeRange(
        *st.slider(
            "Date range",
            min_value=time_range.start,
            max_value=time_range.end,
            value=time_range,
        )
    )

    filtered_bp_df = bp_df[selected_time_range.start : selected_time_range.end]

    draw_all_blood_pressure_charts(filtered_bp_df)
    draw_category_histogram(filtered_bp_df)
    draw_blood_pressure_stage_pies(filtered_bp_df)
    draw_weight_chart(filtered_bp_df)


if __name__ == "__main__":
    main()
