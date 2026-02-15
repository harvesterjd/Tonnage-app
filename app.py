import streamlit as st
import math
import uuid

st.set_page_config(page_title="Grower Dashboard", layout="wide")
st.title("Grower Production Dashboard")

# -------------------------------
# INIT SESSION STATE
# -------------------------------
if "growers" not in st.session_state:
    st.session_state.growers = []

# -------------------------------
# ADD GROWER
# -------------------------------
st.subheader("Add Grower")

new_grower = st.text_input("Grower Name")

if st.button("Add Grower"):
    if new_grower.strip():
        st.session_state.growers.append({
            "id": str(uuid.uuid4()),
            "name": new_grower,
            "farms": []
        })
        st.rerun()

# -------------------------------
# MAIN APP
# -------------------------------
if st.session_state.growers:

    grower_names = [g["name"] for g in st.session_state.growers]
    selected_name = st.selectbox("Select Grower", grower_names)

    grower = next(g for g in st.session_state.growers if g["name"] == selected_name)

    if st.button("Delete Grower"):
        st.session_state.growers = [g for g in st.session_state.growers if g["id"] != grower["id"]]
        st.rerun()

    st.divider()

    # -------------------------------
    # ADD FARM
    # -------------------------------
    st.subheader("Add Farm")

    new_farm = st.text_input("Farm Name")

    if st.button("Add Farm"):
        if new_farm.strip():
            grower["farms"].append({
                "id": str(uuid.uuid4()),
                "name": new_farm,
                "total": 0.0,
                "cut": 0.0
            })
            st.rerun()

    # -------------------------------
    # SHOW ALL FARMS
    # -------------------------------
    if grower["farms"]:

        st.subheader("Farms")

        for farm in grower["farms"]:

            with st.container():
                col1, col2, col3 = st.columns([3,2,2])

                with col1:
                    st.markdown(f"**{farm['name']}**")

                with col2:
                    farm["total"] = st.number_input(
                        "Total Tonnes",
                        min_value=0.0,
                        value=float(farm["total"]),
                        key=f"total_{farm['id']}"
                    )

                with col3:
                    farm["cut"] = st.number_input(
                        "Tonnes Cut",
                        min_value=0.0,
                        value=float(farm["cut"]),
                        key=f"cut_{farm['id']}"
                    )

                if st.button("Delete Farm", key=f"delete_{farm['id']}"):
                    grower["farms"] = [f for f in grower["farms"] if f["id"] != farm["id"]]
                    st.rerun()

        # -------------------------------
        # GROWER TOTALS
        # -------------------------------
        total_tonnes = sum(f["total"] for f in grower["farms"])
        total_cut = sum(f["cut"] for f in grower["farms"])

        percent_cut = (total_cut / total_tonnes * 100) if total_tonnes > 0 else 0

        st.divider()
        st.subheader("Grower Totals")

        st.write(f"Total Tonnes (All Farms): {total_tonnes:.2f}")
        st.write(f"Total Cut: {total_cut:.2f}")
        st.write(f"% Cut: {percent_cut:.2f}%")

        # -------------------------------
        # TARGET + PRODUCTION SETTINGS
        # -------------------------------
        st.divider()
        st.subheader("Target & Production Settings")
        # Initialize grower production settings if not set
if "target_percent" not in grower:
    grower["target_percent"] = 0.0
if "bin_weight" not in grower:
    grower["bin_weight"] = 0.0
if "bins_per_day" not in grower:
    grower["bins_per_day"] = 0.0

grower["target_percent"] = st.number_input(
    "Grower Target %",
    min_value=0.0,
    max_value=100.0,
    value=float(grower["target_percent"])
)

grower["bin_weight"] = st.number_input(
    "Tonnes per Bin",
    min_value=0.0,
    value=float(grower["bin_weight"])
)

grower["bins_per_day"] = st.number_input(
    "Bins per Day",
    min_value=0.0,
    value=float(grower["bins_per_day"])
)

              



        # -------------------------------
        # CALCULATIONS
        # -------------------------------
        target_tonnes = total_tonnes * target_percent / 100
        tonnes_remaining = max(target_tonnes - total_cut, 0)

        total_bins_required = (tonnes_remaining / bin_weight) if bin_weight > 0 else 0

        days_required = (total_bins_required / bins_per_day) if bins_per_day > 0 else 0

        # -------------------------------
        # RESULTS
        # -------------------------------
        st.divider()
        st.subheader("Target Calculation")

        st.write(f"Target Tonnes: {target_tonnes:.2f}")
        st.write(f"Tonnes Remaining To Target: {tonnes_remaining:.2f}")
        st.write(f"Total Bins Required: {total_bins_required:.2f}")
        st.write(f"Days Required: {math.ceil(days_required) if days_required > 0 else 0}")

        # -------------------------------
        # ADD ONE DAY PRODUCTION (Grower Level)
        # -------------------------------
       if st.button("Add One Day Production (Grower)"):
    daily_tonnes = grower["bin_weight"] * grower["bins_per_day"]

    remaining_to_allocate = daily_tonnes

    for farm in grower["farms"]:
        if remaining_to_allocate <= 0:
            break

        farm_remaining = farm["total"] - farm["cut"]
        allocation = min(farm_remaining, remaining_to_allocate)

        farm["cut"] += allocation
        remaining_to_allocate -= allocation

    st.rerun()


    else:
        st.info("No farms added yet.")

else:
    st.info("No growers added yet.")
