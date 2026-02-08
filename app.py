import streamlit as st

st.set_page_config(page_title="Farm Tonnage & Bin Planning", layout="wide")
st.title("Farm Tonnage & Bin Planning")

# -------------------------
# Initialize session state
# -------------------------
if "farms" not in st.session_state:
    st.session_state.farms = [
        {
            "name": "Farm 1",
            "total_tons": 1000.0,
            "tons_cut": 0.0,
            "target_pct": 20.0,
            "bin_weight": 6.0,
            "bins_per_day": 10.0,
        }
    ]


# -------------------------
# Add farm button
# -------------------------
if st.button("+ Add farm"):
    st.session_state.farms.append(
        {
            "name": f"Farm {len(st.session_state.farms) + 1}",
            "total_tons": 1000.0,
            "tons_cut": 0.0,
            "target_pct": 20.0,
            "bin_weight": 6.0,
            "bins_per_day": 10.0,
        }
    )


# -------------------------
# Tabs per farm
# -------------------------
tabs = st.tabs([farm["name"] for farm in st.session_state.farms])

for i, tab in enumerate(tabs):
    farm = st.session_state.farms[i]

    with tab:
        st.subheader(farm["name"])

        # -------------------------
        # FORM (everything inside)
        # -------------------------
        with st.form(key=f"farm_form_{i}"):

            total_tons = st.number_input(
                "Total tons",
                value=farm["total_tons"],
                step=1.0,
            )

            target_pct = st.number_input(
                "Target % to remove",
                value=farm["target_pct"],
                step=0.1,
                format="%.2f",
            )

            tons_cut = st.number_input(
                "Tons cut (manual override allowed)",
                value=farm["tons_cut"],
                step=1.0,
                format="%.2f",
            )

            bin_weight = st.number_input(
                "Bin weight (tons)",
                value=farm["bin_weight"],
                step=0.1,
                format="%.2f",
            )

            bins_per_day = st.number_input(
                "Bins per day",
                value=farm["bins_per_day"],
                step=0.1,
                format="%.2f",
            )

            col1, col2 = st.columns(2)

            apply_pct = col1.form_submit_button("Apply %")
            save_manual = col2.form_submit_button("Save Manual")

        # -------------------------
        # Apply logic AFTER submit
        # -------------------------
        if apply_pct:
            farm["tons_cut"] = total_tons * target_pct / 100
        elif save_manual:
            farm["tons_cut"] = tons_cut

        farm["total_tons"] = total_tons
        farm["target_pct"] = target_pct
        farm["bin_weight"] = bin_weight
        farm["bins_per_day"] = bins_per_day

        tons_remaining = farm["total_tons"] - farm["tons_cut"]
        pct_remaining = (
            (tons_remaining / farm["total_tons"]) * 100
            if farm["total_tons"] > 0
            else 0
        )

        bins_required = (
            farm["tons_cut"] / farm["bin_weight"]
            if farm["bin_weight"] > 0
            else 0
        )

        days_required = (
            bins_required / farm["bins_per_day"]
            if farm["bins_per_day"] > 0
            else 0
        )

        st.divider()
        st.metric("Tons remaining", f"{tons_remaining:.2f}")
        st.metric("% remaining", f"{pct_remaining:.2f}%")
        st.metric("Bins required", f"{bins_required:.2f}")
        st.metric("Days required", f"{days_required:.2f}")
