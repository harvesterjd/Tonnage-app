
import streamlit as st

st.set_page_config(page_title="Farm Tonnage & Bin Planning", layout="wide")

st.title("Farm Tonnage & Bin Planning")

# ---------- Session state ----------
if "farms" not in st.session_state:
    st.session_state.farms = [
        {
            "name": "Farm 1",
            "total_tons": 10000.0,
            "tons_cut": 0.0,
            "bin_weight": 10.0,
            "bins_per_day": 20.0,
            "target_pct": 10.0,
        }
    ]

# ---------- Add farm ----------
if st.button("➕ Add farm"):
    st.session_state.farms.append(
        {
            "name": f"Farm {len(st.session_state.farms) + 1}",
            "total_tons": 10000.0,
            "tons_cut": 0.0,
            "bin_weight": 10.0,
            "bins_per_day": 20.0,
            "target_pct": 10.0,
        }
    )

# ---------- Tabs ----------
tabs = st.tabs([farm["name"] for farm in st.session_state.farms])

for idx, tab in enumerate(tabs):
    farm = st.session_state.farms[idx]

    with tab:
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

            farm["target_pct"] = st.number_input(
                "Target % to remove",
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
                step=0.5,
                format="%.2f",
                key=f"binwt_{idx}",
            )

            farm["bins_per_day"] = st.number_input(
                "Bins allocated per day",
                min_value=0.01,
                value=farm["bins_per_day"],
                step=1.0,
                format="%.2f",
                key=f"binsday_{idx}",
            )

        # ---------- Manual cumulative tons cut ----------
        farm["tons_cut"] = st.number_input(
            "Total tons cut (cumulative)",
            min_value=0.0,
            max_value=farm["total_tons"],
            value=farm["tons_cut"],
            step=10.0,
            format="%.2f",
            key=f"cut_{idx}",
        )

        # ---------- Buttons ----------
        bcol1, bcol2 = st.columns(2)

        with bcol1:
            if st.button("Apply %", key=f"apply_{idx}"):
                additional_cut = farm["total_tons"] * (farm["target_pct"] / 100)
                farm["tons_cut"] = min(
                    farm["tons_cut"] + additional_cut,
                    farm["total_tons"],
                )

        with bcol2:
            if st.button("Reset cumulative tons", key=f"reset_{idx}"):
                farm["tons_cut"] = 0.0

        # ---------- Calculations ----------
        tons_remaining = max(
            farm["total_tons"] - farm["tons_cut"],
            0.0,
        )

        pct_cut_actual = (
            (farm["tons_cut"] / farm["total_tons"]) * 100
            if farm["total_tons"] > 0
            else 0.0
        )

        # Planning calculations (based on target %)
        planned_cut = farm["total_tons"] * (farm["target_pct"] / 100)

        bins_required = (
            planned_cut / farm["bin_weight"]
            if farm["bin_weight"] > 0
            else 0.0
        )

        days_required = (
            bins_required / farm["bins_per_day"]
            if farm["bins_per_day"] > 0
            else 0.0
        )

        # ---------- Metrics ----------
        m1, m2, m3, m4, m5 = st.columns(5)

        m1.metric("Total tons cut", f"{farm['tons_cut']:.2f}")
        m2.metric("% cut", f"{pct_cut_actual:.2f}%")
        m3.metric("Tons remaining", f"{tons_remaining:.2f}")
        m4.metric("Bins required (target %)", f"{bins_required:.2f}")
        m5.metric("Days required", f"{days_required:.2f}")
