import streamlit as st

st.set_page_config(page_title="Diagnostic Test", layout="wide")
st.title("Diagnostic: Percent → Tons Cut")

total_tons = st.number_input(
    "Total tons",
    min_value=0.0,
    value=1000.0,
    step=1.0
)

target_percent = st.number_input(
    "Target % to remove",
    min_value=0.0,
    max_value=100.0,
    value=20.0,
    step=0.1
)

tons_cut = total_tons * (target_percent / 100)

st.markdown("---")
st.metric("Tons cut (cal
