import streamlit as st
import math
import uuid

st.title("Farm Tonnage Tracker")

# -------------------------------------------------
# Initialize farm list
# -------------------------------------------------
if "farms" not in st.session_state:
    st.session_state.farms = []

# -------------------------------------------------
# Add Farm Section
# -------------------------------------------------
st.subheader("Add New Farm")
new_farm_name = st.text_input("Farm Number")

if st.button("Add Farm"):
    if new_farm_name.strip():

        farm_id = str(uuid.uuid4())

        st.session_state.farms.append({
            "id": farm_id,
            "name": new_farm_name
        })

# -------------------------------------------------
# Main Farm Section
# -------------------------------------------------
if st.session_state.farms:

    farm_names = [farm["name"] for farm in st.session_state.farms]
    selected_name = st.selectbox("Select Farm", farm_names)

    farm = next(f for f in st.session_state.farms if f["name"] == selected_name)
    farm_id = farm["id"]

    # -------------------------------------------------
    # Ensure internal storage keys exist
    # -------------------------------------------------
    defaults = {
        f"total_val_{farm_id}": 0.0,
        f"cut_val_{farm_id}": 0.0,
        f"target_val_{farm_id}": 0.0,
        f"tpb_val_{farm_id}": 0.0,
        f"bpd_val_{farm_id}": 0.0,
        f"days_val_{farm_id}": 0,
    }

    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

    st.subheader(f"Farm {selected_name}")

    # -------------------------------------------------
    # Inputs (Safe Pattern)
    # -------------------------------------------------
    total = st.number_input(
        "Total Tonnes",
        min_value=0.0,
        value=st.session_state[f"total_val_{farm_id}"],
        key=f"total_widget_{farm_id}"
    )
    st.session_state[f"total_val_{farm_id}"] = total

    cut = st.number_input(
        "Tonnes Cut",
        min_value=0.0,
        value=st.session_state[f"cut_val_{farm_id}"],
        key=f"cut_widget_{farm_id}"
    )
    st.session_state[f"cut_val_{farm_id}"] = cut

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

    # -------------------------------------------------
    # Add One Day Production (Safe Update)
    # -------------------------------------------------
    if st.button("Add One Day Production"):

        daily = tpb * bpd

        st.session_state[f"cut_val_{farm_id}"] = min(
            st.session_state[f"cut_val_{farm_id}"] + daily,
            st.session_state[f"total_val_{farm_id}"]
        )

        st.rerun()

    st.divider()

    days = st.number_input(
        "Days Planned (Projection)",
        min_value=0,
        step=1,
        value=st.session_state[f"days_val_{farm_id}"],
        key=f"days_widget_{farm_id}"
    )
    st.session_state[f"days_val_{farm_id}"] = days

    # -------------------------------------------------
    # Calculations
    # -------------------------------------------------
    total = st.session_state[f"total_val_{farm_id}"]
    cut = st.session_state[f"cut_val_{farm_id}"]
    target = st.session_state[f"target_val_{farm_id}"]
    tpb = st.session_state[f"tpb_val_{farm_id}"]
    bpd = st.session_state[f"bpd_val_{farm_id}"]
    days = st.session_state[f"days_val_{farm_id}"]

    remaining = total - cut
    percent_cut = (cut / total * 100) if total > 0 else 0

    target_tonnes = total * target / 100
    tonnes_needed = max(target_tonnes - cut, 0)

    bins_required = tonnes_needed / tpb if tpb > 0 else 0
    days_required = bins_required / bpd if bpd > 0 else 0

    projected_tonnes = days * bpd * tpb
    projected_total_cut = min(cut + projected_tonnes, total)
    projected_percent = (projected_total_cut / total * 100) if total > 0 else 0

    # -------------------------------------------------
    # Display Results
    # -------------------------------------------------
    st.write(f"Tonnes Remaining: {remaining:.2f}")
    st.write(f"% Cut: {percent_cut:.2f}%")

    st.divider()

    st.write(f"Target Tonnes ({target}%): {target_tonnes:.2f}")
    st.write(f"Tonnes Required to Reach Target: {tonnes_needed:.2f}")
    st.write(f"Bins Required: {math.ceil(bins_required) if bins_required > 0 else 0}")
    st.write(f"Days Required: {days_required:.2f}")

    st.divider()

    st.subheader("Projection Based on Days")
    st.write(f"Projected Additional Tonnes: {projected_tonnes:.2f}")
    st.write(f"Projected Total Cut: {projected_total_cut:.2f}")
    st.write(f"Projected % Cut: {projected_percent:.2f}%")

else:
    st.info("No farms added yet.")
