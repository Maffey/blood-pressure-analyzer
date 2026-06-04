import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from blood_pressure_analyzer.data_model import ColumnNames


def draw_blood_pressure_chart(df: pd.DataFrame) -> None:
    st.subheader("Blood Pressure & Pulse")

    st.markdown("""
    **Hint:** Use the checkbox below to show standard medical ranges. 
    *You can also click on the names in the legend on the right side of the chart to turn specific lines on or off interactively!*
    """)

    col1, col2 = st.columns([1, 3])
    with col1:
        show_ranges = st.checkbox("Show Medical Ranges (AHA Guidelines)", value=True)

    # --- 4. CREATE THE PLOTLY CHART ---
    # We use make_subplots to create a secondary y-axis for the Pulse (bpm)
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add Systolic Line
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df[ColumnNames.SYSTOLIC],
            name="Systolic (mmHg)", mode='lines+markers',
            line=dict(color='firebrick', width=2),
            marker=dict(size=6)
        ),
        secondary_y=False,
    )

    # Add Diastolic Line
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df[ColumnNames.DIASTOLIC],
            name="Diastolic (mmHg)", mode='lines+markers',
            line=dict(color='royalblue', width=2),
            marker=dict(size=6)
        ),
        secondary_y=False,
    )

    # Add Pulse Line (Secondary Axis)
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df[ColumnNames.PULSE],
            name="Pulse (bpm)", mode='lines+markers',
            line=dict(color='mediumseagreen', dash='dot', width=2),
            marker=dict(size=6)
        ),
        secondary_y=True,
    )

    # --- 5. ADD MEDICAL RANGES (OPTIONAL) ---
    if show_ranges:
        # Based on the American Heart Association (AHA) guidelines for Systolic blood pressure
        # We use add_hrect to add horizontal color bands spanning across the chart

        # Normal (Systolic < 120)
        fig.add_hrect(y0=40, y1=120, line_width=0, fillcolor="green", opacity=0.1,
                      annotation_text="Normal (<120)", annotation_position="top left", secondary_y=False)

        # Elevated (Systolic 120 - 129)
        fig.add_hrect(y0=120, y1=130, line_width=0, fillcolor="yellow", opacity=0.2,
                      annotation_text="Elevated (120-129)", annotation_position="top left", secondary_y=False)

        # High Blood Pressure - Stage 1 (Systolic 130 - 139)
        fig.add_hrect(y0=130, y1=140, line_width=0, fillcolor="orange", opacity=0.2,
                      annotation_text="Stage 1 Hypertension (130-139)", annotation_position="top left",
                      secondary_y=False)

        # High Blood Pressure - Stage 2 (Systolic 140 - 180)
        fig.add_hrect(y0=140, y1=180, line_width=0, fillcolor="red", opacity=0.2,
                      annotation_text="Stage 2 Hypertension (140-180)", annotation_position="top left",
                      secondary_y=False)

        # Hypertensive Crisis (Systolic > 180)
        fig.add_hrect(y0=180, y1=220, line_width=0, fillcolor="darkred", opacity=0.3,
                      annotation_text="Hypertensive Crisis (>180)", annotation_position="top left", secondary_y=False)

    fig.update_layout(
        title="Blood Pressure & Pulse History",
        hovermode="x unified",  # Shows a vertical line with all data points on hover
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=20, r=20, t=60, b=20)
    )

    # Format the Y-Axes
    fig.update_yaxes(title_text="Blood Pressure (mmHg)", range=[40, 200], secondary_y=False)
    fig.update_yaxes(title_text="Pulse (bpm)", range=[40, 150], showgrid=False, secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)