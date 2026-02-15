import streamlit as st
import math
import uuid

st.title("Grower Farm Tonnage Tracker")

# -------------------------------
# INIT SESSION STATE
# -------------------------------
if "growers" not in st.session_state:
    st.session_state.growers = []

# -------------------------------
# ADD GROWER
# -------------------------------
st.subheader("Add New Grower")

new_grower_name = st.text_input("Grower Name", key="grower_input")

if st.button("Add Grower", key="add_grower"):
    if new_grower_name.strip():
        st.session_state.growers.append({
            "id": str(uuid.uuid4()),
            "name": new_grower_name,
            "farms": []
        })
        st.rerun()

# -------------------------------
# MAIN LOGIC
# -------------------------------
if st.session_state.growers:

    grower_names = [g["name"] for g in st.session_state.growers]

    selected_grower_name = st.selectbox(
        "Select Grower",
        grower_names,
        key="grower_select"
    )

    grower = next(g for g in st.session_state.growers if g["name"] == selected_grower_name)

    st.divider()

    # -------------------------------
    # ADD FARM
    # -------------------------------
    st.subheader("Add Farm")

    new_farm_name = st.text_input("Farm Number", key="farm_input")

    if st.button("Add Farm", key="add_farm"):
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

    # -------------------------------
    # FARM SECTION
    # -------------------------------
    if grower["farms"]:

        farm_names = [f["name"] for f in grower["farms"]]

        selected_farm_name = st.selectbox(
            "Select Farm",
            farm_names,
            key="farm_select"
        )

        farm = next(f for f in grower["farms"] if f["name"] == selected_farm_name)

        st.subheader(f"Farm {farm['name']}")

        farm["total"] = st.number_input(
            "Total Tonnes",
            min_value=0.0,
            value=float(farm.get("total", 0.0)),
            key=f"total_{farm['id']}"
        )

        farm["cut"] = st.number_input(
            "Tonnes Cut",
            min_value=0.0,
            value=float(farm.get("cut", 0.0)),
            key=f"cut_{farm['id']}"
        )

        farm["target"] = st.number_input(
            "Target %",
            min_value=0.0,
            max_value=100.0,
            value=float(farm.get("target", 0.0)),
            key=f"target_{farm['id']}"
        )

        st.divider()

        farm["tpb"] = st.number_input(
            "Tonnes per Bin",
            min_value=0.0,
            value=float(farm.get("tpb", 0.0)),
            key=f"tpb_{farm['id']}"
        )

        farm["bpd"] = st.number_input(
            "Bins per Day",
            min_value=0.0,
            value=float(farm.get("bpd", 0.0)),
            key=f"bpd_{farm['id']}"
        )

        if st.button("Add One Day Production", key=f"prod_{farm['id']}"):
            daily = farm["tpb"] * farm["bpd"]
            farm["cut"] = min(farm["cut"] + daily, farm["total"])
            st.rerun()


            st.divider()

            farm["days"] = st.number_input(
            "Days Planned (Projection)",
             min_value=0,
             step=1,
             value=int(farm.get("days", 0)),
             key=f"days_{farm['id']}"
        )

        # -------------------------------
        # FARM CALCULATIONS
        # -------------------------------
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
        days_required = math.ceil(tonnes_needed / daily_capacity) if daily_capacity > 0 else 0

        projected_tonnes = days * daily_capacity
        projected_total_cut = min(cut + projected_tonnes, total)
        projected_percent = (projected_total_cut / total * 100) if total > 0 else 0

        st.write(f"Tonnes Remaining: {remaining:.2f}")
        st.write(f"% Cut (Farm): {percent_cut:.2f}%")

        st.divider()

        st.write(f"Target Tonnes: {target_tonnes:.2f}")
        st.write(f"Tonnes Required: {tonnes_needed:.2f}")
        st.write(f"Days Remaining to Hit Target: {days_required}")

        st.divider()

        st.subheader("Projection")
        st.write(f"Projected Total Cut: {projected_total_cut:.2f}")
        st.write(f"Projected % Cut: {projected_percent:.2f}%")

        st.divider()

        # -------------------------------
        # GROWER TOTALS
        # -------------------------------
        total_grower_tonnes = sum(f["total"] for f in grower["farms"])
        total_grower_cut = sum(f["cut"] for f in grower["farms"])

        total_grower_target_tonnes = sum(
            f["total"] * f["target"] / 100 for f in grower["farms"]
        )

        grower_percent_cut = (
            (total_grower_cut / total_grower_tonnes) * 100
            if total_grower_tonnes > 0 else 0
        )

        grower_target_progress = (
            (total_grower_cut / total_grower_target_tonnes) * 100
            if total_grower_target_tonnes > 0 else 0
        )

        st.subheader("Grower Totals")
        st.write(f"Total Tonnes: {total_grower_tonnes:.2f}")
        st.write(f"Total Cut: {total_grower_cut:.2f}")
        st.write(f"% Cut: {grower_percent_cut:.2f}%")
        st.write(f"Target Progress: {grower_target_progress:.2f}%")

    else:
        st.info("No farms added yet.")

else:
    st.info("No growers added yet.")
