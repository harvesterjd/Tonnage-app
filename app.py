import streamlit as st

st.title("Farm Tonnage Calculator")

# Inputs
farm_number = st.text_input("Farm Number / Name")

total_tonnes = st.number_input("Total Tonnes", min_value=0.0)

tonnes_cut = st.number_input("Tonnes Cut", min_value=0.0)

# Calculations
tonnes_remaining = total_tonnes - tonnes_cut

if total_tonnes > 0:
    percent_cut = (tonnes_cut / total_tonnes) * 100
else:
    percent_cut = 0.0

# Outputs
st.write("Tonnes Remaining:", tonnes_remaining)
st.write("Percent Cut:", percent_cut)
