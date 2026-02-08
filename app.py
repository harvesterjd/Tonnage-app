import streamlit as st

st.set_page_config(page_title="Single Farm Test", layout="wide")
st.title("Single Farm – Working Override Test")

# ----------------------
# Inputs
# ----------------------
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

# Store tons_cut in session state
if "tons_cut" not in st.session_state:
    st.session_state.tons_cut = total_tons * (target_percent / 100)

# Recalculate when % changes
calculated_cut = total_tons * (target_percent / 100)
if abs(calculated_cut - st.session_state.tons_cut) > 0.001:
    st.session_state.tons_cut = calculated_cut

# Manual override
tons_cut = st.number_input(
    "Tons cut (editable)",
    min_value=0.0,
    value=st.session_state.tons_cut,
    step=1.0
)

st.session_state.tons_cut = tons_cut

# ----------------------
# Results
# ----------------------
tons_remaining = total_tons - tons_cut
percent_cut = (tons_cut / total_tons * 100) if total_tons > 0 else 0

st.markdown("---")
st.metric("Tons remaining", f"{tons_remaining:.2f}")
st.metric("% cut", f"{percent_cut:.2f}%")
