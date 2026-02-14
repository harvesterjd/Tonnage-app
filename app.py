import streamlit as st

st.set_page_config(page_title="Simple Tonnage Test")

st.title("Farm Tonnage – Back to Basics")

# ---- Inputs ----
farm_name = st.text_input("Farm name", "Farm 1")

total_tons = st.number_input(
    "Total tons",
    min_value=0.0,
    value=10000.0,
)

tons_cut = st.number_input(
    "Tons cut (cumulative)",
    min_value=0.0,
    value=0.0,
)

target_percent = st.number_input(
    "Target %",
    min_value=0.0,
    max_value=100.0,
    value=10.0,
)

# ---- Calculations ----
tons_remaining = max(total_tons - tons_cut, 0)

percent_cut = (tons_cut / total_tons * 100) if total_tons > 0 else 0

projected_cut = tons_remaining * (target_percent / 100)

# ---- Output ----
st.divider()

st.write(f"### Results for {farm_name}")

st.write("Tons remaining:", round(tons_remaining, 2))
st.write("Percent cut:", round(percent_cut, 2), "%")
st.write("Projected tons to remove:", round(projected_cut, 2))
