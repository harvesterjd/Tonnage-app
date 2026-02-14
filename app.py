import streamlit as st

st.set_page_config(page_title="Farm Tonnage Calculator")

st.title("Farm Tonnage Calculator")

# -----------------------
# INPUT BOXES
# -----------------------

farm_number = st.text_input("Farm Number / Name")

total_tonnes = st.number_input(
    "Total Tonnes",
    min_value=0.0,
    value=0.0,
    step=100.0,
)

tonnes_cut = st.number_input(
    "Tonnes Cut",
    min_value=0.0,
    value=0.0,
    step=10.0,
)

# -----------------------
# CALCULATIONS
# -----------------------

tonnes_remaining = total_tonnes - tonnes_cut

if total_tonnes > 0:
    percent_cut = (tonnes_cut / total_tonnes) * 100
else:
    percent_cut = 0.0

# Prevent negative remaining
if tonnes_remaining < 0:
    tonnes_remaining = 0.0

# -----------------------
# OUTPUT BOXES
# -----------------------

st.number_input(
    "Tonnes Remaining",
    value=tonnes_remaining,
    disabled=True,
)

st.number_input(
    "% Cut",
    value=percent_cut,
    disabled=True,
)
