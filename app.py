import streamlit as st
import math
import uuid

st.title("Farm Tonnage Tracker")

if "farms" not in st.session_state:
    st.session_state.farms = []

# -----------------------------
# Add Farm
# -----------------------------
st.subheader("Add New Farm")
new_farm_name = st.text_input("Farm Number")

if st.button("Add Farm"):
    if new_farm_name.strip():
        farm_id = str(uuid.uuid4())

        st.session_state.farms.append({
            "id": farm_id,
            "name": new_farm_name
        })

        # Internal storage (NOT widget keys)
        st.session_state[f"total_val_{farm_id}"] = 0.0
        st.session_state[f"cut_val_{farm_id}"] = 0.0
        st.session_state[f"target_val_{farm_id}"] = 0.0
        st.session_state[f"tpb_val_{farm_id}"] = 0.0
        st.session_state[f"bpd_val_{farm_id}"] = 0.0
        st.session_state[f"days_val_{farm_id}"] = 0

# -----------------------------
# Select Farm
# -----------------------------
if st.session_state.farms:

    farm_names = [farm["name"] for farm in st.session_state.farms]
    selected_name = st.selectbox("Select Farm", farm_names)

    farm = next(f for f in st.session_state.farms if f["name"] == selected_name)
    farm_id = farm["id"]

    st.subheader(f"Farm {selected_name}")

    # ---- TOTAL ----
    total = st.number_input(
        "Total Tonnes",
        min_value=0.0,
        value=st.session_state[f"total_val_{farm_id}"],
        key=f"total_widget_{farm_id}"
    )
    st.session_state[f"total_val_{farm_id}"] = total

    # ---- CUT ----
    cut = st.number_input(
        "Tonnes Cut",
        min_value=0.0,
        value=st.session_state[f"cut_val_{farm_id}"],
        key=f"cut_widget_{farm_id}"
    )
    st.session_state[f"cut_val_{farm_id}"] = cut

    # ---- TARGET ----
    target = st.number_input(
        "Target %",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state[f"target_val_{farm_id}"],
        key=f"target_widget_{farm_id}"
    )
    st.session_state[f"target_val_{farm_id}"] = target

    st.divider()

    tpb = st.number_input(
        "Tonnes per Bin",
        min_value=0.0,
        value=st.session_state[f"tpb_val_{farm_id}"],
        key=f"tpb_widget_{farm_id}"
    )
    st.session_state[f"tpb_val_{farm_id}"] = tpb

    bpd = st.number_input(
        "Bins per Day",
        min_value=0.0,
        value=st.session_state[f"bpd_val_{farm_id}"],
        key=f"bpd_widget_{farm_id}"
    )
    st.session_state[f"bpd_val_{farm_id}"] = bpd

    # ---- SAFE UPDATE ----
    if st.button("Add One Day Production"):

        daily = tpb * bpd

        st.session_state[f"cut_val_{farm_id}"] = min(
            st.session_state[f"cut_val_{farm_id}"] + daily,
            st.session_state[f"total_val_{farm_id}"]
        )

        st.rerun()

    st.divider()

    # Calculations
    total = st.session_state[f"total_val_{farm_id}"]
    cut = st.session_state[f"cut_val_{farm_id}"]

    remaining = total - cut
    percent_cut = (cut / total * 100) if total > 0 else 0

    st.write(f"Tonnes Remaining: {remaining:.2f}")
    st.write(f"% Cut: {percent_cut:.2f}")

else:
    st.info("No farms added yet.")
