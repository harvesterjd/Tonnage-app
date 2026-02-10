import streamlit as st

st.set_page_config(page_title="Farm Tonnage & Bin Planning", layout="wide")
st.title("Farm Tonnage & Bin Planning")

# ---------- Initialise ----------
if "farms" not in st.session_state:
    st.session_state.farms = [
        {
            "farm_name": "Farm 1",
            "total_tons": 10000.0,
            "tons_cut": 0.0,
            "target_pct": 10.0,
            "bin_weight": 10.0,
            "bins_per_day": 20.0,
        }
    ]

# ---------- Add farm ----------
if st.button("➕ Add farm"):
    st.session_state.farms.append(
        {
            "farm_name": f"Farm {len(st.session_state.farms) + 1}",
            "total_tons": 10000.0,
            "tons_cut": 0.0,
            "target_pct": 10.0,
            "bin_weight": 10.0,
            "bins_per_day": 20.0,
        }
    )

# ---------- Tabs ----------
tabs = st.tabs([farm["farm_name"] for farm in st.session_state.farms])

# ---------- Helper functions ----------
def apply_target(idx):
    farm = st.session_state.farms[idx]
    remaining = max(farm["total_tons"] - farm["tons_cut"], 0.0)
    cut = remaining * (farm["target_pct"] / 100)
    farm["tons_cut"] = min(farm["tons_cut"] + cut, farm["total_tons"])

def reset_cut(idx):
    st.session_state.farms[idx]["tons_cut"] = 0.0

# ---------- Per farm ----------
for idx, tab in enumerate(tabs):
    farm = st.session_state.farms[idx]

    with tab:
        st.subheader("Farm details")

        farm["farm_name"] = st.text_input(
            "Farm number / name",
            farm["farm_name"],
            key=f"name_{idx}",
        )

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
                "Target % to remove (of remaining)",
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

        # ---------- Tons cut (safe) ----------
        farm["tons_cut"] = st.number_input(
            "Tons cut (cumulative)",
            min_value=0.0,
            max_value=farm["total_tons"],
            value=farm["tons_cut"],
            step=10.0,
            format="%.2f",
            key=f"cut_{idx}",
        )

        # ---------- Calculations ----------
        tons_remaining = max(farm["total_tons"] - farm["tons_cut"], 0.0)

        pct_cut_actual = (
            (farm["tons_cut"] / farm["total_tons"]) * 100
            if farm["total_tons"] > 0
            else 0.0
        )

        projected_cut = tons_remaining * (farm["target_pct"] / 100)

        bins_required = (
            projected_cut / farm["bin_weight"]
            if farm["bin_weight"] > 0
            else 0.0
        )

        days_required = (
            bins_required / farm["bins_per_day"]
            if farm["bins_per_day"] > 0
            else 0.0
        )

        # ---------- Buttons ----------
        b1, b2 = st.columns(2)

        with b1:
            st.button(
                "Apply target %",
                on_click=apply_target,
                args=(idx,),
                disabled=tons_remaining <= 0,
            )

        with b2:
            st.button(
                "Reset cumulative tons",
                on_click=reset_cut,
                args=(idx,),
            )

        # ---------- Metrics ----------
        m1, m2, m3, m4, m5 = st.columns(5)

        m1.metric("Tons cut (total)", f"{farm['tons_cut']:.2f}")
        m2.metric("% cut", f"{pct_cut_actual:.2f}%")
        m3.metric("Tons remaining", f"{tons_remaining:.2f}")
        m4.metric("Projected tons to remove", f"{projected_cut:.2f}")
        m5.metric("Days required", f"{days_required:.2f}")
