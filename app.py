import streamlit as st
import json
import os

DATA_FILE = "data.json"

# ---------------------------
# Load or initialize data
# ---------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"growers": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

st.title("Tonnage Tracker")

# ---------------------------
# Add Grower
# ---------------------------
st.header("Add Grower")

new_grower = st.text_input("Grower Name")

if st.button("Add Grower"):
    if new_grower:
        if new_grower not in data["growers"]:
            data["growers"][new_grower] = []
            save_data(data)
            st.success("Grower added")
        else:
            st.warning("Grower already exists")

st.divider()

# ---------------------------
# Select Grower
# ---------------------------
if data["growers"]:
    selected_grower = st.selectbox(
        "Select Grower",
        list(data["growers"].keys())
    )

    st.header("Add Load")

    tonnage = st.number_input("Tonnage", min_value=0.0, step=0.1)

    if st.button("Add Load"):
        data["growers"][selected_grower].append(tonnage)
        save_data(data)
        st.success("Load added")

    st.divider()

    st.header("Summary")

    loads = data["growers"][selected_grower]
    total = sum(loads)

    st.write("Number of Loads:", len(loads))
    st.write("Total Tonnage:", total)

    if loads:
        st.bar_chart(loads)

else:
    st.info("Add a grower to begin.")
