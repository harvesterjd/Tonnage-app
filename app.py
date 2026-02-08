import streamlit as st

st.set_page_config(page_title="Farm Tonnage Planner", layout="wide")
st.title("Farm Tonnage & Bin Planning")

# -------------------------
# Initialise farms
# -------------------------
if "farms" not in st.session_state:
    st.session_state.farms = {
        "Farm 1": {
            "total_tons": 1000.0,
            "target_percent": 20.0,
            "bin_weight": 10.0,
            "bins_per_day": 10.0,
        }
    }
    st.session_state["Farm 1_cut"] = 0.0

# -------------------------
# Add farm
# -------------------------
if st.button("➕ Add farm"):
    n = len(st.session_state.farms) + 1
    name = f"Farm {n}"
    st.session_state.farms[name] = {
        "total_tons": 1000.0,
        "target_percent": 20.0,
        "bin_weight": 10.0,
        "bins_per_day": 10.0,
    }
    st.session_state[f"{name}_cut"] = 0.0

# -------------------------
# Tabs
# -------------------------
tabs = st.tabs(list(st.session_state.farms.keys()))

for tab, (farm_name, farm) in zip(tabs, st.session_state.farms.items()):
    with tab:
        st.subheader(farm_name)

        cut_key = f"{farm_name}_cut"

        c1, c2, c3 = st.columns(3)

        # -------- Column 1: Inputs + APPLY BUTTON FIRST --------
        with c1:
            farm["total_tons"] = st.number_input(
                "Total tons",
                min_value=0.0,
                step=1.0,
                key=f"{farm_name}_total"
            )

            farm["target_percent"] = st.number_input(
                "Target % to remove",
                min_value=0.0,
                max_value=100.0,
                step=0.1,
                key=f"{farm_name}_percent"
            )

            if st.button("Apply %", key=f"{farm_name}_apply"):
                st.session_state[cut_key] = (
                    farm["total_tons"] * farm["target_percent"] / 100
                )

        # -------- Column 2: Tons cut (created ONCE) --------
        with c2:
            st.number_input(
                "Tons cut",
                min_value=0.0,
                step=1.0,
                key=cut_key
            )

            tons_cut = st.session_state[cut_key]
            tons_remaining = farm["total_tons"] - tons_cut
            percent_cut = (
                (tons_cut / farm["total_tons"]) * 100
                if farm["total_tons"] > 0 else 0
            )

            st.metric("Tons remaining", f"{tons_remaining:.2f}")
            st.metric("% cut", f"{percent_cut:.2f}%")

        # -------- Column 3: Bins --------
        with c3:
            farm["bin_weight"] = st.number_input(
                "Bin weight (tons)",
                min_value=0.1,
                step=0.1,
                key=f"{farm_name}_bin_weight"
            )

            farm["bins_per_day"] = st.number_input(
                "Bins per day",
                min_value=0.1,
                step=0.1,
                key=f"{farm_name}_bins_day"
            )

            required_bins = (
                tons_cut / farm["bin_weight"]
                if farm["bin_weight"] > 0 else 0
            )

            days_required = (
                required_bins / farm["bins_per_day"]
                if farm["bins_per_day"] > 0 else 0
            )

            st.metric("Required bins", f"{required_bins:.2f}")
            st.metric("Days required", f"{days_required:.2f}")
