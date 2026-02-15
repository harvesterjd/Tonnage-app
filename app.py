import streamlit as st
import json
import os
import uuid

DATA_FILE = "data.json"


# -----------------------------
# Load Data Safely
# -----------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"growers": []}

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {"growers": []}
            if "growers" not in data:
                data["growers"] = []
            return data
    except:
        return {"growers": []}


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.data, f, indent=4)


# -----------------------------
# Initialise Session
# -----------------------------
if "data" not in st.session_state:
    st.session_state.data = load_data()


# -----------------------------
# App Title
# -----------------------------
st.title("Tonnage Tracker")


# -----------------------------
# Add Grower
# -----------------------------
st.header("Add Grower")

with st.form("add_grower"):
    grower_name = st.text_input("Grower Name")
    bin_weight = st.number_input("Bin Weight (tonnes)", min_value=0.0)
    bins_per_day = st.number_input("Bins Per Day", min_value=0.0)

    submitted = st.form_submit_button("Add Grower")

    if submitted and grower_name:
        st.session_state.data["growers"].append({
            "id": str(uuid.uuid4()),
            "name": grower_name,
            "bin_weight": bin_weight,
            "bins_per_day": bins_per_day,
            "farms": []
        })
        save_data()
        st.success("Grower Added")
        st.rerun()


# -----------------------------
# Display Growers
# -----------------------------
for grower in st.session_state.data["growers"]:

    st.divider()
    st.subheader(grower["name"])

    # Add Farm
    with st.form(f"add_farm_{grower['id']}"):
        farm_name = st.text_input("Farm Name", key=f"name_{grower['id']}")
        total_tonnes = st.number_input(
            "Total Tonnes",
            min_value=0.0,
            key=f"total_{grower['id']}"
        )

        add_farm = st.form_submit_button("Add Farm")

        if add_farm and farm_name:
            grower["farms"].append({
                "id": str(uuid.uuid4()),
                "name": farm_name,
                "total": total_tonnes,
                "cut": 0.0
            })
            save_data()
            st.rerun()

    # -----------------------------
    # Farms
    # -----------------------------
   for farm in grower["farms"]:

    st.markdown(f"### {farm['name']}")
    st.write(f"Total Tonnes: {farm['total']}")

    step = grower["bin_weight"] * grower["bins_per_day"]
    cut_key = f"cut_{farm['id']}"

    # Initialise once
    if cut_key not in st.session_state:
        st.session_state[cut_key] = float(farm.get("cut", 0))

    # Buttons FIRST (before number_input)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕", key=f"plus_{farm['id']}"):
            if step > 0:
                st.session_state[cut_key] = min(
                    st.session_state[cut_key] + step,
                    farm["total"]
                )

    with col2:
        if st.button("➖", key=f"minus_{farm['id']}"):
            if step > 0:
                st.session_state[cut_key] = max(
                    st.session_state[cut_key] - step,
                    0
                )

    # THEN the widget
    st.number_input(
        "Tonnes Cut",
        min_value=0.0,
        max_value=float(farm["total"]),
        key=cut_key
    )

    farm["cut"] = st.session_state[cut_key]

    remaining = farm["total"] - farm["cut"]
    st.write(f"Remaining: {remaining}")

save_data()

