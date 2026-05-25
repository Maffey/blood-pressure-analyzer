import streamlit as st

from blood_pressure_analyzer.csv_parser import parse_blood_pressure_csv


def main():
    st.title("Blood Pressure Analyzer")
    bp_df = parse_blood_pressure_csv("input_data/Mateusz_20250212_20260525.csv")
    xd = 5


if __name__ == "__main__":
    main()
