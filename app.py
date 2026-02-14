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
        st.session_state.farms.append({"id": farm_id, "name": new_farm_name})

        st.session_state[f"total_{farm_id}"] = 0.0
        st.session_state[f"cut_{farm_id}"] = 0.0
        st.session_state[f"target_{farm_id}"] = 0.0
        st.session_state[f"tpb_{farm_id}"] = 0.0
        st.session_state[f"bpd_{farm_id}"] = 0.0
        st.session_state[f"days_{farm_id}"] = 0

# -----------------------------
# Select Farm Instead of Tabs
# -----------------------------
if st.session_state.farms:

    farm_names = [farm["name"] for farm in st.session_state.farms]
    selected_name = st.selectbox("Select Farm", farm_names)

    selected_farm = next(
        farm for farm in st.session_state.farms
        if farm["name"] == selected_name
    )

    farm_id = selected_farm["id"]

    st.subheader(f"Farm {selected_name}")

    # Inputs
    st.number_input("Total Tonnes", min_value=0.0, key=f"total_{farm_id}")
    st.number_input("Tonnes Cut", min_value=0.0, key=f"cut_{farm_id}")
    st.number_input("Target %", min_value=0.0, max_value=100.0, key=f"target_{farm_id}")

    st.divider()

    st.number_input("Tonnes per Bin", min_value=0.0, key=f"tpb_{farm_id}")
    st.number_input("Bins per Day", min_value=0.0, key=f"bpd_{farm_id}")

    if st.button("Add One Day Production"):

        daily = (
            st.session_state[f"tpb_{farm_id}"] *
            st.session_state[f"bpd_{farm_id}"]
        )

        st.session_state[f"cut_{farm_id}"] = min(
            st.session_state[f"cut_{farm_id}"] + daily,
            st.session_state[f"total_{farm_id}"]
        )

        st.success(f"Added {daily:.2f} tonnes.")

    st.divider()

    st.number_input("Days Planned (Projection)", min_value=0, step=1, key=f"days_{farm_id}")

    # Calculations
    total = st.session_state[f"total_{farm_id}"]
    cut = st.session_state[f"cut_{farm_id}"]
    target_percent = st.session_state[f"target_{farm_id}"]
    tpb = st.session_state[f"tpb_{farm_id}"]
    bpd = st.session_state[f"bpd_{farm_id}"]
    days = st.session_state[f"days_{farm_id}"]

    remaining = total - cut
    percent_cut = (cut / total * 100) if total > 0 else 0

    target_tonnes = total * target_percent / 100
    tonnes_needed = max(target_tonnes - cut, 0)

    bins_required = tonnes_needed / tpb if tpb > 0 else 0
    days_required = bins_required / bpd if bpd > 0 else 0

    projected_tonnes = days * bpd * tpb
    projected_total_cut = min(cut + projected_tonnes, total)
    projected_percent = (projected_total_cut / total * 100) if total > 0 else 0

    st.write(f"Tonnes Remaining: {remaining:.2f}")
    st.write(f"% Cut: {percent_cut:.2f}%")

    st.divider()

    st.write(f"Target Tonnes ({target_percent}%): {target_tonnes:.2f}")
    st.write(f"Tonnes Required: {tonnes_needed:.2f}")
    st.write(f"Bins Required: {math.ceil(bins_required) if bins_required > 0 else 0}")
    st.write(f"Days Required: {days_required:.2f}")

    st.divider()

    st.subheader("Projection")
    st.write(f"Projected Additional Tonnes: {projected_tonnes:.2f}")
    st.write(f"Projected Total Cut: {projected_total_cut:.2f}")
    st.write(f"Projected % Cut: {projected_percent:.2f}")

else:
    st.info("No farms added yet.")
