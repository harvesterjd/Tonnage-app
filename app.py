import streamlit as st
import math
import uuid

st.title("Grower Farm Tonnage Tracker")

# -------------------------------------------------
# Initialize
# -------------------------------------------------
if "growers" not in st.session_state:
    st.session_state.growers = []

# -------------------------------------------------
# Add Grower
# -------------------------------------------------
st.subheader("Add New Grower")
new_grower_name = st.text_input("Grower Name")

if st.button("Add Grower"):
    if new_grower_name.strip():

        grower_id = str(uuid.uuid4())

        st.session_state.growers.append({
            "id": grower_id,
            "name": new_grower_name,
            "farms": []
        })

# -------------------------------------------------
# Main Section
# -------------------------------------------------
if st.session_state.growers:

    grower_names = [g["name"] for g in st.session_state.growers]
    selected_grower_name = st.selectbox("Select Grower", grower_names)

    grower = next(g for g in st.session_state.growers if g["name"] == selected_grower_name)
    grower_id = grower["id"]

    # -------------------------------------------------
    # Delete Grower
    # -------------------------------------------------
    def delete_grower(grower_id):

        grower = next(g for g in st.session_state.growers if g["id"] == grower_id)

        for farm in grower["farms"]:
            farm_id = farm["id"]

            keys_to_remove = [
                f"total_{farm_id}",
                f"cut_{farm_id}",
                f"target_{farm_id}",
                f"tpb_{farm_id}",
                f"bpd_{farm_id}",
                f"days_{farm_id}",
            ]

            for key in keys_to_remove:
                if key in st.session_state:
                    del st.session_state[key]

        st.session_state.growers = [
            g for g in st.session_state.growers
            if g["id"] != grower_id
        ]

        st.rerun()

    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader(f"Grower: {selected_grower_name}")

    with col2:
        st.button(
            "Delete Grower",
            on_click=delete_grower,
            args=(grower_id,),
            type="secondary"
        )

    st.divider()

    # =================================================
    # 🔥 GROWER AGGREGATED TOTALS (NEW SECTION)
    # =================================================
    total_grower_tonnes = 0
    total_grower_cut = 0
    total_grower_target_tonnes = 0

    for farm in grower["farms"]:
        fid = farm["id"]

        total = st.session_state.get(f"total_{fid}", 0)
        cut = st.session_state.get(f"cut_{fid}", 0)
        target = st.session_state.get(f"target_{fid}", 0)

        total_grower_tonnes += total
        total_grower_cut += cut
        total_grower_target_tonnes += (total * target / 100)

    grower_percent_cut = (
        (total_grower_cut / total_grower_tonnes) * 100
        if total_grower_tonnes > 0 else 0
    )

    grower_target_percent = (
        (total_grower_target_tonnes / total_grower_tonnes) * 100
        if total_grower_tonnes > 0 else 0
    )

    if grower["farms"]:
        st.subheader("Grower Totals (All Farms)")
        st.write(f"Total Grower Tonnes: {total_grower_tonnes:.2f}")
        st.write(f"Total Grower Tonnes Cut: {total_grower_cut:.2f}")
        st.write(f"Total Grower % Cut: {grower_percent_cut:.2f}%")
        st.write(f"Total Grower Target %: {grower_target_percent:.2f}%")
        st.divider()

    # -------------------------------------------------
    # Add Farm
    # -------------------------------------------------
    st.subheader("Add Farm")
    new_farm_name = st.text_input("Farm Number")

    if st.button("Add Farm"):
        if new_farm_name.strip():

            farm_id = str(uuid.uuid4())

            grower["farms"].append({
                "id": farm_id,
                "name": new_farm_name
            })

            st.session_state[f"total_{farm_id}"] = 0.0
            st.session_state[f"cut_{farm_id}"] = 0.0
            st.session_state[f"target_{farm_id}"] = 0.0
            st.session_state[f"tpb_{farm_id}"] = 0.0
            st.session_state[f"bpd_{farm_id}"] = 0.0
            st.session_state[f"days_{farm_id}"] = 0
        st.rerun()

    # -------------------------------------------------
    # Farm Section
    # -------------------------------------------------
    if grower["farms"]:

        farm_names = [f["name"] for f in grower["farms"]]
        selected_farm_name = st.selectbox("Select Farm", farm_names)

        farm = next(f for f in grower["farms"] if f["name"] == selected_farm_name)
        farm_id = farm["id"]

        def add_day(farm_id):
            daily = (
                st.session_state[f"tpb_{farm_id}"] *
                st.session_state[f"bpd_{farm_id}"]
            )

            st.session_state[f"cut_{farm_id}"] = min(
                st.session_state[f"cut_{farm_id}"] + daily,
                st.session_state[f"total_{farm_id}"]
            )

        def delete_farm(farm_id):

            grower["farms"] = [
                f for f in grower["farms"]
                if f["id"] != farm_id
            ]

            keys_to_remove = [
                f"total_{farm_id}",
                f"cut_{farm_id}",
                f"target_{farm_id}",
                f"tpb_{farm_id}",
                f"bpd_{farm_id}",
                f"days_{farm_id}",
            ]

            for key in keys_to_remove:
                if key in st.session_state:
                    del st.session_state[key]

            st.rerun()

        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader(f"Farm {selected_farm_name}")

        with col2:
            st.button(
                "Delete Farm",
                on_click=delete_farm,
                args=(farm_id,),
                type="secondary"
            )

        # Inputs
        st.number_input("Total Tonnes", min_value=0.0, key=f"total_{farm_id}")
        st.number_input("Tonnes Cut", min_value=0.0, key=f"cut_{farm_id}")
        st.number_input("Target %", min_value=0.0, max_value=100.0, key=f"target_{farm_id}")

        st.divider()

        st.number_input("Tonnes per Bin", min_value=0.0, key=f"tpb_{farm_id}")
        st.number_input("Bins per Day", min_value=0.0, key=f"bpd_{farm_id}")

        st.button(
            "Add One Day Production",
            on_click=add_day,
            args=(farm_id,)
        )

        st.divider()

        st.number_input("Days Planned (Projection)", min_value=0, step=1, key=f"days_{farm_id}")

        # Calculations
        total = st.session_state[f"total_{farm_id}"]
        cut = st.session_state[f"cut_{farm_id}"]
        target = st.session_state[f"target_{farm_id}"]
        tpb = st.session_state[f"tpb_{farm_id}"]
        bpd = st.session_state[f"bpd_{farm_id}"]
        days = st.session_state[f"days_{farm_id}"]

        remaining = total - cut
        percent_cut = (cut / total * 100) if total > 0 else 0

        target_tonnes = total * target / 100
        tonnes_needed = max(target_tonnes - cut, 0)

        daily_capacity = tpb * bpd
        bins_required = tonnes_needed / tpb if tpb > 0 else 0

        if daily_capacity > 0:
            days_required = math.ceil(tonnes_needed / daily_capacity)
        else:
            days_required = 0

        projected_tonnes = days * daily_capacity
        projected_total_cut = min(cut + projected_tonnes, total)
        projected_percent = (projected_total_cut / total * 100) if total > 0 else 0

        # Output
        st.write(f"Tonnes Remaining: {remaining:.2f}")
        st.write(f"% Cut (Farm): {percent_cut:.2f}%")

        st.divider()

        st.write(f"Target Tonnes ({target}%): {target_tonnes:.2f}")
        st.write(f"Tonnes Required: {tonnes_needed:.2f}")
        st.write(f"Bins Required: {math.ceil(bins_required) if bins_required > 0 else 0}")
        st.write(f"Days Remaining to Hit Target: {days_required}")

        st.divider()

        st.subheader("Projection")
        st.write(f"Projected Additional Tonnes: {projected_tonnes:.2f}")
        st.write(f"Projected Total Cut: {projected_total_cut:.2f}")
        st.write(f"Projected % Cut: {projected_percent:.2f}%")
# =================================================
# 🔥 GROWER AGGREGATED TOTALS (NEW SECTION)
# =================================================
total_grower_tonnes = 0
total_grower_cut = 0
total_grower_target_tonnes = 0

for farm in grower["farms"]:
    fid = farm["id"]

    total = st.session_state.get(f"total_{fid}", 0)
    cut = st.session_state.get(f"cut_{fid}", 0)
    target = st.session_state.get(f"target_{fid}", 0)

    total_grower_tonnes += total
    total_grower_cut += cut
    total_grower_target_tonnes += (total * target / 100)

grower_percent_cut = (
    (total_grower_cut / total_grower_tonnes) * 100
    if total_grower_tonnes > 0 else 0
)

grower_target_percent = (
    (total_grower_target_tonnes / total_grower_tonnes) * 100
    if total_grower_tonnes > 0 else 0
)

if grower["farms"]:
    st.subheader("Grower Totals (All Farms)")
    st.write(f"Total Grower Tonnes: {total_grower_tonnes:.2f}")
    st.write(f"Total Grower Tonnes Cut: {total_grower_cut:.2f}")
    st.write(f"Total Grower % Cut: {grower_percent_cut:.2f}%")
    st.write(f"Total Grower Target %: {grower_target_percent:.2f}%")
    st.divider()

    else:
        st.info("No farms added for this grower yet.")

else:
    st.info("No growers added yet.")
