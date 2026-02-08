import streamlit as st

st.set_page_config(page_title="Farm Tonnage & Bin Planning", layout="wide")

st.title("Farm Tonnage & Bin Planning")

# -------------------------
# Session state setup
# -------------------------
if "farms" not in st.session_state:
    st.session_state.farms = [
        {
            "name": "Farm 1",
            "total_tons": 10000.0,
            "tons_cut": 0.0,
            "target_pct": 10.0,
            "bin_weight": 5.0,
            "bins_per_day": 50.0,
        }
    ]

# -------------------------
# Add farm button
# -------------------------
if st.button("➕ Add farm"):
    farm_number = len(st.session_state.farms) + 1
    st.session_state.farms.append(
        {
            "name": f"Farm {farm_number}",
            "total_tons": 10000.0,
            "tons_cut": 0.0,
            "target_pct": 10.0,
            "bin_weight": 5.0,
            "bins_per_day": 50.0,
        }
    )

# -------------------------
# Tabs per farm
# -------------------------
tabs = st.tabs([farm["name"] for farm in st.session_state.farms])

for idx, tab in enumerate(tabs):
    with tab:
        farm = st.session_state.farms[idx]

        st.subheader(farm["name"])

        col1, col2 = st.columns(2)

        with col1:
            farm["total_tons"] = st.number_input(
                "Total tons",
                min_value=0.0,
                value=farm["total_tons"],
                step=100.0,
                format="%.2f",
                key=f"total_{idx}",
            )

            farm["tons_cut"] = st.number_input(
                "Tons cut (manual)",
                min_value=0.0,
                value=farm["tons_cut"],
                step=10.0,
                format="%.2f",
                key=f"cut_{idx}",
            )

            farm["target_pct"] = st.number_input(
                "Target % cut (cumulative)",
                min_value=0.0,
                max_value=100.0,
                value=farm["target_pct"],
                step=1.0,
                format="%.2f",
                key=f"pct_{idx}",
            )

        with col2:
            farm["bin_weight"] = st.number_input(
                "Bin weight (tons)",
                min_value=0.01,
                value=farm["bin_weight"],
                step=0.1,
                format="%.2f",
                key=f"binwt_{idx}",
            )

            farm["bins_per_day"] = st.number_input(
                "Bins per day",
                min_value=0.0,
                value=farm["bins_per_day"],
                step=1.0,
                format="%.2f",
                key=f"binsday_{idx}",
            )

        st.divider()

        # -------------------------
        # Calculations
        # -------------------------
        total_required_cut = farm["total_tons"] * farm["target_pct"] / 100

        this_round_cut = max(
            total_required_cut - farm["tons_cut"],
            0.0
        )

        pct_cut_actual = (
            (farm["tons_cut"] / farm["total_tons"]) * 100
            if farm["total_tons"] > 0
            else 0.0
        )

        bins_required = (
            this_round_cut / farm["bin_weight"]
            if farm["bin_weight"] > 0
            else 0.0
        )

        days_required = (
            bins_required / farm["bins_per_day"]
            if farm["bins_per_day"] > 0
            else 0.0
        )

        # -------------------------
        # Display metrics
        # -------------------------
        m1, m2, m3, m4, m5 = st.columns(5)

        m1.metric("Cumulative tons cut", f"{farm['tons_cut']:.2f}")
        m2.metric("% cut", f"{pct_cut_actual:.2f}%")
        m3.metric("Tons to cut this round", f"{this_round_cut:.2f}")
        m4.metric("Bins required (this round)", f"{bins_required:.2f}")
        m5.metric("Days required", f"{days_required:.2f}")
