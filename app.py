import streamlit as st
import json
import os
import uuid

DATA_FILE = "data.json"

# -----------------------------
# Load Data
# -----------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"growers": []}

# -----------------------------
# Save Data
# -----------------------------
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.data, f, indent=4)

# -----------------------------
# Initialise
# -----------------------------
if "data" not in st.session_state:
    st.session_state.data = load_data()

st.title("Tonnage Planner")

# -----------------------------
# Add Grower
# -----------------------------
st.subheader("Add Grower")
new_grower = st.text_input("Grower Name")

if st.button("Add Grower"):
    if new_grower.strip() != "":
        st.session_state.data["growers"].append({
            "id": str(uuid.uuid4()),
            "name": new_grower,
            "target_percent": 0,
            "bin_weight": 0,
            "bins_per_day": 0,
            "farms": []
        })
        save_data()
        st.rerun()

st.divider()

# -----------------------------
# Grower Loop
# -----------------------------
for grower in st.session_state.data["growers"]:

    with st.expander(grower["name"], expanded=True):

        # -----------------------------
        # Grower Settings
        # -----------------------------
        c1, c2, c3 = st.columns(3)

        with c1:
            grower["target_percent"] = st.number_input(
                "Target %",
                min_value=0.0,
                max_value=100.0,
                value=float(grower.get("target_percent", 0)),
                key=f"target_{grower['id']}"
            )

        with c2:
            grower["bin_weight"] = st.number_input(
                "Bin Weight",
                min_value=0.0,
                value=float(grower.get("bin_weight", 0)),
                key=f"binweight_{grower['id']}"
            )

        with c3:
            grower["bins_per_day"] = st.number_input(
                "Bins Per Day",
                min_value=0.0,
                value=float(grower.get("bins_per_day", 0)),
                key=f"binsperday_{grower['id']}"
            )

        # -----------------------------
        # Add Farm
        # -----------------------------
        new_farm = st.text_input(
            "New Farm Name",
            key=f"newfarm_{grower['id']}"
        )

        if st.button("Add Farm", key=f"addfarm_{grower['id']}"):
            if new_farm.strip() != "":
                grower["farms"].append({
                    "id": str(uuid.uuid4()),
                    "name": new_farm,
                    "total": 0,
                    "cut": 0
                })
                save_data()
                st.rerun()

        st.divider()

        # -----------------------------
        # Farm Loop
        # -----------------------------
        total_tonnes = 0

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
                    value=float(farm.get("total", 0)),
                    key=f"total_{farm['id']}"
                )

            # Tonnes Cut + Buttons
            with col3:

                step = grower["bin_weight"] * grower["bins_per_day"]
                cut_key = f"cut_{farm['id']}"

                if cut_key not in st.session_state:
                    st.session_state[cut_key] = float(farm.get("cut", 0))

                c1, c2, c3 = st.columns([3, 1, 1])

                # Tonnes Cut input
                with c1:
                    st.number_input(
                        "Tonnes Cut",
                        min_value=0.0,
                        max_value=float(farm["total"]),
                        key=cut_key
                    )

                # PLUS
                with c2:
                    if st.button("➕", key=f"plus_{farm['id']}"):
                        if step > 0:
                            st.session_state[cut_key] = min(
                                st.session_state[cut_key] + step,
                                farm["total"]
                            )
                            save_data()
                            st.rerun()

                # MINUS
                with c3:
                    if st.button("➖", key=f"minus_{farm['id']}"):
                        if step > 0:
                            st.session_state[cut_key] = max(
                                st.session_state[cut_key] - step,
                                0
                            )
                            save_data()
                            st.rerun()

                farm["cut"] = st.session_state[cut_key]

            total_tonnes += farm["total"]

            # Delete Farm
            if st.button("Delete Farm", key=f"deletefarm_{farm['id']}"):
                grower["farms"] = [
                    f for f in grower["farms"]
                    if f["id"] != farm["id"]
                ]
                save_data()
                st.rerun()

            st.divider()

        # -----------------------------
        # Calculations
        # -----------------------------
        target_tonnes = total_tonnes * grower["target_percent"] / 100

        total_bins_required = 0
        days_required = 0

        if grower["bin_weight"] > 0:
            total_bins_required = target_tonnes / grower["bin_weight"]

        if grower["bins_per_day"] > 0:
            days_required = total_bins_required / grower["bins_per_day"]

        st.markdown(f"### Total Tonnes: {total_tonnes:.2f}")
        st.markdown(f"### Target Tonnes: {target_tonnes:.2f}")
        st.markdown(f"### Total Bins Required: {total_bins_required:.2f}")
        st.markdown(f"### Days Required: {days_required:.2f}")

        # Delete Grower
        if st.button("Delete Grower", key=f"deletegrower_{grower['id']}"):
            st.session_state.data["growers"] = [
                g for g in st.session_state.data["growers"]
                if g["id"] != grower["id"]
            ]
            save_data()
            st.rerun()
