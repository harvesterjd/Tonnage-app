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
    farm_num = len(st.session_state.farms) + 1
    st.session_state.farms.append(
        {
            "name": f"Farm {farm_num}",
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

for idx, tab in enumerate(tabs):
    farm = st.session_state.farms[idx]

    # Unique keys per farm
    cut_key = f"tons_cut_{idx}"

    if cut_key not in st.session_state:
        st.session_state[cut_key] = farm["tons_cut"]

    with tab:
        st.subheader(farm["name"])

        farm["total_tons"] = st.number_input(
            "Total tons",
            value=farm["total_tons"],
            step=1.0,
            key=f"total_{idx}",
        )

        farm["target_pct"] = st.number_input(
            "Target % to remove",
            value=farm["target_pct"],
            step=0.1,
            format="%.2f",
            key=f"target_{idx}",
        )

        if st.button("Apply %", key=f"apply_{idx}"):
            st.session_state[cut_key] = farm["total_tons"] * farm["target_pct"] / 100

        # Manual override ALWAYS allowed
        st.number_input(
    "Tons cut",
    value=st.session_state[cut_key],
    step=1.0,
    format="%.2f",
    key=f"cut_input_{idx}",
    on_change=lambda i=idx: st.session_state.update(
        {f"tons_cut_{i}": st.session_state[f"cut_input_{i}"]}
    ),
)
            "Tons cut",
            value=st.session_state[cut_key],
            step=1.0,
            format="%.2f",
            key=f"cut_input_{idx}",
        )

        tons_remaining = farm["total_tons"] - st.session_state[cut_key]
        pct_remaining = (
            (tons_remaining / farm["total_tons"]) * 100
            if farm["total_tons"] > 0
            else 0
        )

        st.metric("Tons remaining", f"{tons_remaining:.2f}")
        st.metric("% remaining", f"{pct_remaining:.2f}%")

        st.divider()

        farm["bin_weight"] = st.number_input(
            "Bin weight (tons)",
            value=farm["bin_weight"],
            step=0.1,
            format="%.2f",
            key=f"bin_weight_{idx}",
        )

        farm["bins_per_day"] = st.number_input(
            "Bins per day",
            value=farm["bins_per_day"],
            step=0.1,
            format="%.2f",
            key=f"bins_day_{idx}",
        )

        bins_required = (
            st.session_state[cut_key] / farm["bin_weight"]
            if farm["bin_weight"] > 0
            else 0
        )

        days_required = (
            bins_required / farm["bins_per_day"]
            if farm["bins_per_day"] > 0
            else 0
        )

        st.metric("Bins required", f"{bins_required:.2f}")
        st.metric("Days required", f"{days_required:.2f}")
