import streamlit as st
import math
import uuid

st.title("Grower Farm Tonnage Tracker")

# =================================================
# INITIALIZE
# =================================================
if "growers" not in st.session_state:
    st.session_state.growers = []

# =================================================
# ADD GROWER
# =================================================
st.subheader("Add New Grower")
new_grower_name = st.text_input("Grower Name")

if st.button("Add Grower"):
    if new_grower_name.strip():
        st.session_state.growers.append({
            "id": str(uuid.uuid4()),
            "name": new_grower_name,
            "farms": []
        })
        st.rerun()

# =================================================
# MAIN SECTION
# =================================================
if st.session_state.growers:

    grower_names = [g["name"] for g in st.session_state.growers]
    selected_grower_name = st.selectbox("Select Grower", grower_names)

    grower = next(g for g in st.session_state.growers if g["name"] == selected_grower_name)
# -------------------------------------------------
# Upgrade ALL farms safely (prevents KeyError)
# -------------------------------------------------
defaults = {
    "total": 0.0,
    "cut": 0.0,
    "target": 0.0,
    "tpb": 0.0,
    "bpd": 0.0,
    "days": 0
}

for farm in grower["farms"]:
    for key, value in defaults.items():
        if key not in farm:
            farm[key] = value

    st.divider()

    # =================================================
    # ADD FARM
    # =================================================
    st.subheader("Add Farm")
    new_farm_name = st.text_input("Farm Number")

    if st.button("Add Farm"):
        if new_farm_name.strip():
            grower["farms"].append({
                "id": str(uuid.uuid4()),
                "name": new_farm_name,
                "total": 0.0,
                "cut": 0.0,
                "target": 0.0,
                "tpb": 0.0,
                "bpd": 0.0,
                "days": 0
            })
            st.rerun()

    # =================================================
    # FARM SECTION
    # =================================================
    if grower["farms"]:

        farm_names = [f["name"] for f in grower["farms"]]
        selected_farm_name = st.selectbox("Select Farm", farm_names)

        farm = next(f for f in grower["farms"] if f["name"] == selected_farm_name)

        # -------------------------------------------------
        # SAFETY UPGRADE (handles old farms)
        # -------------------------------------------------
        defaults = {
            "total": 0.0,
            "cut": 0.0,
            "target": 0.0,
            "tpb": 0.0,
            "bpd": 0.0,
            "days": 0
        }

        for key, value in defaults.items():
            if key not in farm:
                farm[key] = value

        st.subheader(f"Farm {farm['name']}")

        # ---------------- Inputs ----------------
        farm["total"] = st.number_input(
            "Total Tonnes",
            min_value=0.0,
            value=float(farm["total"])
        )

        farm["cut"] = st.number_input(
            "Tonnes Cut",
            min_value=0.0,
            value=float(farm["cut"])
        )

        farm["target"] = st.number_input(
            "Target %",
            min_value=0.0,
            max_value=100.0,
            value=float(farm["target"])
        )

        st.divider()

        farm["tpb"] = st.number_input(
            "Tonnes per Bin",
            min_value=0.0,
            value=float(farm["tpb"])
        )

        farm["bpd"] = st.number_input(
            "Bins per Day",
            min_value=0.0,
            value=float(farm["bpd"])
        )

        if st.button("Add One Day Production"):
            daily = farm["tpb"] * farm["bpd"]
            farm["cut"] = min(farm["cut"] + daily, farm["total"])
            st.rerun()

        st.divider()

        farm["days"] = st.number_input(
            "Days Planned (Projection)",
            min_value=0,
            step=1,
            value=int(farm["days"])
        )

        # =================================================
        # FARM CALCULATIONS
        # =================================================
        total = farm["total"]
        cut = farm["cut"]
        target = farm["target"]
        tpb = farm["tpb"]
        bpd = farm["bpd"]
        days = farm["days"]

        remaining = total - cut
        percent_cut = (cut / total * 100) if total > 0 else 0

        target_tonnes = total * target / 100
        tonnes_needed = max(target_tonnes - cut, 0)

        daily_capacity = tpb * bpd
        bins_required = tonnes_needed / tpb if tpb > 0 else 0
        days_required = math.ceil(tonnes_needed / daily_capacity) if daily_capacity > 0 else 0

        projected_tonnes = days * daily_capacity
        projected_total_cut = min(cut + projected_tonnes, total)
        projected_percent = (projected_total_cut / total * 100) if total > 0 else 0

        # ---------------- Output ----------------
        st.write(f"Tonnes Remaining: {remaining:.2f}")
        st.write(f"% Cut (Farm): {percent_cut:.2f}%")

        st.divider()

        st.write(f"Target Tonnes ({target}%): {target_tonnes:.2f}")
        st.write(f"Tonnes Required: {tonnes_needed:.2f}")
        st.write(f"Bins Required: {math.ceil(bins_required) if bins_required > 0 else 0}")
        st.write(f"Days Remaining to Hit Target: {days_required}")

        st.divider()

        st.subheader("Projection")
        st.write(f"Projected Additional Tonnes: {projected_tonnes:.2f}")
        st.write(f"Projected Total Cut: {projected_total_cut:.2f}")
        st.write(f"Projected % Cut: {projected_percent:.2f}%")

        st.divider()

# =================================================
# GROWER TOTALS (100% SAFE)
# =================================================
total_grower_tonnes = sum(f.get("total", 0.0) for f in grower["farms"])
total_grower_cut = sum(f.get("cut", 0.0) for f in grower["farms"])
total_grower_target_tonnes = sum(
    f.get("total", 0.0) * f.get("target", 0.0) / 100
    for f in grower["farms"]
)

grower_percent_cut = (
    (total_grower_cut / total_grower_tonnes) * 100
    if total_grower_tonnes > 0 else 0
)

grower_target_percent = (
    (total_grower_target_tonnes / total_grower_tonnes) * 100
    if total_grower_tonnes > 0 else 0
)

st.subheader("Grower Totals (All Farms)")
st.write(f"Total Grower Tonnes: {total_grower_tonnes:.2f}")
st.write(f"Total Grower Tonnes Cut: {total_grower_cut:.2f}")
st.write(f"Total Grower % Cut: {grower_percent_cut:.2f}%")
st.write(f"Total Grower Target %: {grower_target_percent:.2f}%")
