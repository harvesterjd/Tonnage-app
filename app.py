import streamlit as st

st.set_page_config(page_title="Farm Tonnage Planner", layout="wide")
st.title("Farm Tonnage & Bin Planning")

# ----------------------
# Initialize farms
# ----------------------
if "farms" not in st.session_state:
    st.session_state.farms = {
        "Farm 1": {
            "total_tons": 1000.0,
            "target_percent": 20.0,
            "tons_cut": None,
            "bin_weight": 1.0,
            "bins_per_day": 10.0
        }
    }

# ----------------------
# Sidebar: add farm
# ----------------------
st.sidebar.header("Farms")

if st.sidebar.button("➕ Add farm"):
    n = len(st.session_state.farms) + 1
    st.session_state.farms[f"Farm {n}"] = {
        "total_tons": 0.0,
        "target_percent": 20.0,
        "tons_cut": None,
        "bin_weight": 1.0,
        "bins_per_day": 10.0
    }

# ----------------------
# Farm tabs
# ----------------------
tabs = st.tabs(list(st.session_state.farms.keys()))

for tab, farm_name in zip(tabs, st.session_state.farms.keys()):
    with tab:
        farm = st.session_state.farms[farm_name]
        st.subheader(farm_name)

        c1, c2, c3 = st.columns(3)

 # -------- Inputs --------
        with c1:
            farm["total_tons"] = st.number_input(
                "Total tons",
                min_value=0.0,
                value=farm["total_tons"],
                step=1.0,
                key=f"{farm_name}_total"
            )

            farm["target_percent"] = st.number_input(
                "Target % to remove",
                min_value=0.0,
                max_value=100.0,
                value=farm["target_percent"],
                step=0.1,
                key=f"{farm_name}_percent"
            )

        # -------- Working override logic --------
        calculated_cut = farm["total_tons"] * (farm["target_percent"] / 100)

        if farm["tons_cut"] is None:
            farm["tons_cut"] = calculated_cut
        elif abs(calculated_cut - farm["tons_cut"]) > 0.001:
            farm["tons_cut"] = calculated_cut

        with c2:
            farm["tons_cut"] = st.number_input(
                "Tons cut (editable)",
                min_value=0.0,
                value=farm["tons_cut"],
                step=1.0,
                key=f"{farm_name}_cut"
            )

        with c3:
            farm["bin_weight"] = st.number_input(
                "Bin weight (tons)",
                min_value=0.0,
                value=farm["bin_weight"],
                step=0.1,
                key=f"{farm_name}_bin"
            )

            farm["bins_per_day"] = st.number_input(
                "Bins per day",
                min_value=0.0,
                value=farm["bins_per_day"],
                step=1.0,
                key=f"{farm_name}_bins_day"
            )

        # -------- Calculations --------
        tons_remaining = farm["total_tons"] - farm["tons_cut"]

        percent_cut = (
            (farm["tons_cut"] / farm["total_tons"]) * 100
            if farm["total_tons"] > 0 else 0
        )

        required_bins = (
            farm["tons_cut"] / farm["bin_weight"]
            if farm["bin_weight"] > 0 else 0
        )

        days_required = (
            required_bins / farm["bins_per_day"]
            if farm["bins_per_day"] > 0 else 0
        )

        # -------- Results --------
        st.markdown("---")
        r1, r2, r3, r4 = st.columns(4)

        r1.metric("Tons remaining", f"{tons_remaining:.2f}")
        r2.metric("% cut", f"{percent_cut:.2f}%")
        r3.metric("Required bins", f"{required_bins:.2f}")
        r4.metric("Days required", f"{days_required:.2f}")
