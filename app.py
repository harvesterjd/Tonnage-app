import streamlit as st

st.set_page_config(page_title="Farm Tonnage Calculator")

st.title("Farm Tonnage Calculator")

# -----------------------
# SESSION STATE
# -----------------------

if "farms" not in st.session_state:
    st.session_state.farms = [
        {"name": "Farm 1", "total": 0.0, "cut": 0.0}
    ]

# -----------------------
# ADD FARM BUTTON
# -----------------------

if st.button("➕ Add Farm"):
    farm_number = len(st.session_state.farms) + 1
    st.session_state.farms.append(
        {"name": f"Farm {farm_number}", "total": 0.0, "cut": 0.0}
    )

# -----------------------
# CREATE TABS
# -----------------------

tabs = st.tabs([farm["name"] for farm in st.session_state.farms])

# -----------------------
# FARM LOOP
# -----------------------

for i, farm in enumerate(st.session_state.farms):

    with tabs[i]:

        # Inputs
        farm["name"] = st.text_input(
            "Farm Number / Name",
            farm["name"],
            key=f"name_{i}"
        )

        farm["total"] = st.number_input(
            "Total Tonnes",
            min_value=0.0,
            value=farm["total"],
            key=f"total_{i}"
        )

        farm["cut"] = st.number_input(
            "Tonnes Cut",
            min_value=0.0,
            value=farm["cut"],
            key=f"cut_{i}"
        )

        # Calculations
        tonnes_remaining = farm["total"] - farm["cut"]

        if farm["total"] > 0:
            percent_cut = (farm["cut"] / farm["total"]) * 100
        else:
            percent_cut = 0.0

        if tonnes_remaining < 0:
            tonnes_remaining = 0.0

        # Outputs
        st.write("Tonnes Remaining:", tonnes_remaining)
        st.write("Percent Cut:", percent_cut)
