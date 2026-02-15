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
        json.dump(st.session_state.growers, f, indent=4)


# -----------------------------
# INIT STATE
# -----------------------------
if "growers" not in st.session_state:
    st.session_state.growers = load_data()


# -----------------------------
# ADD GROWER
# -----------------------------
st.subheader("Add Grower")
new_grower_name = st.text_input("Grower Name", key="new_grower")

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
    new_farm_name = st.text_input("Farm Name", key="new_farm")

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

            st.markdown(f"### {farm['name']}")

            col1, col2, col3 = st.columns(3)

            # TOTAL TONNES
            with col1:
                farm["total"] = st.number_input(
                    "Total Tonnes",
                    min_value=0.0,
                    value=float(farm["total"]),
                    key=f"total_{farm['id']}"
                )

            # CUT TONNES
            with col2:
                farm["cut"] = st.number_input(
                    "Tonnes Cut",
                    min_value=0.0,
                    max_value=float(farm["total"]),
                    value=float(farm["cut"]),
                    key=f"cut_{farm['id']}"
                )

            # PLUS / MINUS
            with col3:

                step = grower["bin_weight"] * grower["bins_per_day"]

                if st.button("➕ Add Day", key=f"plus_{farm['id']}"):
                    if step > 0:
                        farm["cut"] = min(farm["cut"] + step, farm["total"])
                        save_data()
                        st.rerun()

                if st.button("➖ Remove Day", key=f"minus_{farm['id']}"):
                    if step > 0:
                        farm["cut"] = max(farm["cut"] - step, 0)
                        save_data()
                        st.rerun()

            # DELETE FARM
            if st.button("Delete Farm", key=f"delete_{farm['id']}"):
                grower["farms"] = [
                    f for f in grower["farms"]
                    if f["id"] != farm["id"]
                ]
                save_data()
                st.rerun()

            st.divider()

        save_data()

        # -----------------------------
        # TOTALS
        # -----------------------------
        total_tonnes = sum(f["total"] for f in grower["farms"])
        total_cut = sum(f["cut"] for f in grower["farms"])
        percent_cut = (total_cut / total_tonnes * 100) if total_tonnes > 0 else 0

        st.subheader("Grower Totals")

        colA, colB, colC = st.columns(3)
        colA.metric("Total Tonnes", f"{total_tonnes:.2f}")
        colB.metric("Total Cut", f"{total_cut:.2f}")
        colC.metric("% Cut", f"{percent_cut:.2f}%")

        # -----------------------------
        # TARGET SETTINGS
        # -----------------------------
        st.divider()
        st.subheader("Target & Production")

        col1, col2, col3 = st.columns(3)

        with col1:
            grower["target_percent"] = st.number_input(
                "Target %",
                min_value=0.0,
                max_value=100.0,
                value=float(grower["target_percent"])
            )

        with col2:
            grower["bin_weight"] = st.number_input(
                "Tonnes per Bin",
                min_value=0.0,
                value=float(grower["bin_weight"])
            )

        with col3:
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

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Target Tonnes", f"{target_tonnes:.2f}")
        col2.metric("Tonnes Remaining", f"{tonnes_remaining:.2f}")
        col3.metric("Bins Required", f"{total_bins_required:.2f}")
        col4.metric("Days Required", math.ceil(days_required) if days_required > 0 else 0)

    else:
        st.info("No farms added yet.")

else:
    st.info("No growers added yet.")
