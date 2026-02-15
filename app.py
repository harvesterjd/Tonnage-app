import streamlit as st
import math
import uuid
import json
import os

st.set_page_config(page_title="Grower Dashboard", layout="wide")
st.title("Grower Production Dashboard")

DATA_FILE = "data.json"

# -----------------------------
# LOAD / SAVE
# -----------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.growers, f)

# -----------------------------
# INIT STATE
# -----------------------------
if "growers" not in st.session_state:
    st.session_state.growers = load_data()

# -----------------------------
# ADD GROWER
# -----------------------------
st.subheader("Add Grower")
new_grower_name = st.text_input("Grower Name")

if st.button("Add Grower"):
    if new_grower_name.strip():
        st.session_state.growers.append({
            "id": str(uuid.uuid4()),
            "name": new_grower_name,
            "farms": [],
            "target_percent": 0.0,
            "bin_weight": 0.0,
            "bins_per_day": 0.0
        })
        save_data()
        st.rerun()

# -----------------------------
# SELECT GROWER
# -----------------------------
if st.session_state.growers:

    grower_names = [g["name"] for g in st.session_state.growers]
    selected_name = st.selectbox("Select Grower", grower_names)

    grower = next(g for g in st.session_state.growers if g["name"] == selected_name)

    st.divider()

    # DELETE GROWER
    if st.button("Delete Grower"):
        st.session_state.growers = [
            g for g in st.session_state.growers
            if g["id"] != grower["id"]
        ]
        save_data()
        st.rerun()

    # -----------------------------
    # ADD FARM
    # -----------------------------
    st.subheader("Add Farm")
    new_farm_name = st.text_input("Farm Name")

    if st.button("Add Farm"):
        if new_farm_name.strip():
            grower["farms"].append({
                "id": str(uuid.uuid4()),
                "name": new_farm_name,
                "total": 0.0,
                "cut": 0.0
            })
            save_data()
            st.rerun()

    # -----------------------------
    # FARMS
    # -----------------------------
    if grower["farms"]:

        st.subheader("Farms")

        for farm in grower["farms"]:

            col1, col2, col3 = st.columns(3)

            # Farm Name
            with col1:
                st.markdown(f"**{farm['name']}**")

            # Total Tonnes
            with col2:
                farm["total"] = st.number_input(
                    "Total Tonnes",
                    min_value=0.0,
                    value=float(farm["total"]),
                    key=f"total_{farm['id']}"
                )

            # Tonnes Cut + +/- Buttons
            with col3:

                step = grower["bin_weight"] * grower["bins_per_day"]

                c1, c2, c3 = st.columns([3, 1, 1])

                # Tonnes Cut box
                step = grower["bin_weight"] * grower["bins_per_day"]

cut_key = f"cut_{farm['id']}"

# Ensure key exists
if cut_key not in st.session_state:
    st.session_state[cut_key] = float(farm["cut"])

c1, c2, c3 = st.columns([3, 1, 1])

# Tonnes Cut box
with c1:
    st.number_input(
        "Tonnes Cut",
        min_value=0.0,
        max_value=float(farm["total"]),
        key=cut_key
    )

# PLUS button
with c2:
    if st.button("➕", key=f"plus_{farm['id']}"):
        if step > 0:
            st.session_state[cut_key] = min(
                st.session_state[cut_key] + step,
                farm["total"]
            )
            save_data()
            st.rerun()

# MINUS button
with c3:
    if st.button("➖", key=f"minus_{farm['id']}"):
        if step > 0:
            st.session_state[cut_key] = max(
                st.session_state[cut_key] - step,
                0
            )
            save_data()
            st.rerun()

# Sync back into farm data
farm["cut"] = st.session_state[cut_key]

            # DELETE FARM
            if st.button("Delete Farm", key=f"delete_{farm['id']}"):
                grower["farms"] = [
                    f for f in grower["farms"]
                    if f["id"] != farm["id"]
                ]
                save_data()
                st.rerun()

        # -----------------------------
        # TOTALS
        # -----------------------------
        total_tonnes = sum(f["total"] for f in grower["farms"])
        total_cut = sum(f["cut"] for f in grower["farms"])

        percent_cut = (total_cut / total_tonnes * 100) if total_tonnes > 0 else 0

        st.divider()
        st.subheader("Grower Totals")

        st.write(f"Total Tonnes: {total_tonnes:.2f}")
        st.write(f"Total Cut: {total_cut:.2f}")
        st.write(f"% Cut: {percent_cut:.2f}%")

        # -----------------------------
        # TARGET SETTINGS
        # -----------------------------
        st.divider()
        st.subheader("Target & Production")

        grower["target_percent"] = st.number_input(
            "Target %",
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

        save_data()

        # -----------------------------
        # CALCULATIONS
        # -----------------------------
        target_tonnes = total_tonnes * grower["target_percent"] / 100
        tonnes_remaining = max(target_tonnes - total_cut, 0)

        total_bins_required = (
            tonnes_remaining / grower["bin_weight"]
            if grower["bin_weight"] > 0 else 0
        )

        days_required = (
            total_bins_required / grower["bins_per_day"]
            if grower["bins_per_day"] > 0 else 0
        )

        st.divider()
        st.subheader("Target Calculation")

        st.write(f"Target Tonnes: {target_tonnes:.2f}")
        st.write(f"Tonnes Remaining: {tonnes_remaining:.2f}")
        st.write(f"Total Bins Required: {total_bins_required:.2f}")
        st.write(f"Days Required: {math.ceil(days_required) if days_required > 0 else 0}")

    else:
        st.info("No farms added yet.")

else:
    st.info("No growers added yet.")
