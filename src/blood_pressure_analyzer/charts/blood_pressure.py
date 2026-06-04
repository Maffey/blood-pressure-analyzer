import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from blood_pressure_analyzer.data_model import ColumnNames


def draw_blood_pressure_chart(df: pd.DataFrame) -> None:
    st.subheader("Blood Pressure & Pulse")
    st.markdown("**Hint:** Use the switch below to show standard medical ranges.")

    range_selection = st.radio(
        "Show Medical Ranges (AHA Guidelines):",
        options=["None", ColumnNames.SYSTOLIC, ColumnNames.DIASTOLIC],
        horizontal=True
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # SYS
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df[ColumnNames.SYSTOLIC],
            name="Systolic (mmHg)", mode='lines+markers',
            line=dict(color='firebrick', width=2),
            marker=dict(size=6)
        ),
        secondary_y=False,
    )

    # DIA
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df[ColumnNames.DIASTOLIC],
            name="Diastolic (mmHg)", mode='lines+markers',
            line=dict(color='royalblue', width=2),
            marker=dict(size=6)
        ),
        secondary_y=False,
    )

    # Pulse
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df[ColumnNames.PULSE],
            name="Pulse (bpm)", mode='lines+markers',
            line=dict(color='mediumseagreen', dash='dot', width=2),
            marker=dict(size=6)
        ),
        secondary_y=True,
    )

    if range_selection == ColumnNames.SYSTOLIC:
        # TODO refactor this part into reusable components
        # AHA Guidelines for Systolic blood pressure (Annotations on the Left)
        fig.add_hrect(y0=40, y1=120, line_width=0, fillcolor="green", opacity=0.1,
                      annotation_text="Sys Normal (<120)", annotation_position="top left", secondary_y=False)

        fig.add_hrect(y0=120, y1=130, line_width=0, fillcolor="yellow", opacity=0.2,
                      annotation_text="Sys Elevated (120-129)", annotation_position="top left", secondary_y=False)

        fig.add_hrect(y0=130, y1=140, line_width=0, fillcolor="orange", opacity=0.2,
                      annotation_text="Sys Stage 1 Hypertension (130-139)", annotation_position="top left", secondary_y=False)

        fig.add_hrect(y0=140, y1=180, line_width=0, fillcolor="red", opacity=0.2,
                      annotation_text="Sys Stage 2 Hypertension (140-180)", annotation_position="top left", secondary_y=False)

        fig.add_hrect(y0=180, y1=220, line_width=0, fillcolor="darkred", opacity=0.3,
                      annotation_text="Sys Severe Hypertension (>180)", annotation_position="top left", secondary_y=False)

    if range_selection == ColumnNames.DIASTOLIC:
        # AHA Guidelines for Diastolic blood pressure (Annotations on the Right to avoid overlap)
        # Note: There is no "Elevated" category for Diastolic, it jumps from Normal (<80) to Stage 1 (80-89)
        fig.add_hrect(y0=40, y1=80, line_width=0, fillcolor="green", opacity=0.1,
                      annotation_text="Dia Normal (<80)", annotation_position="top right", secondary_y=False)

        fig.add_hrect(y0=80, y1=90, line_width=0, fillcolor="orange", opacity=0.2,
                      annotation_text="Dia Stage 1 Hypertension (80-89)", annotation_position="top right", secondary_y=False)

        fig.add_hrect(y0=90, y1=120, line_width=0, fillcolor="red", opacity=0.2,
                      annotation_text="Dia Stage 2 Hypertension (90-120)", annotation_position="top right", secondary_y=False)

        fig.add_hrect(y0=120, y1=220, line_width=0, fillcolor="darkred", opacity=0.3,
                      annotation_text="Dia Severe Hypertension (>120)", annotation_position="top right", secondary_y=False)

    # --- CHART FORMATTING ---
    fig.update_layout(
        title="Blood Pressure & Pulse History",
        hovermode="x unified",
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
    fig.update_yaxes(title_text="Blood Pressure (mmHg)", range=[40, 220], secondary_y=False)
    fig.update_yaxes(title_text="Pulse (bpm)", range=[40, 150], showgrid=False, secondary_y=True)

    st.plotly_chart(fig, width="stretch")