import streamlit as st
import math
import uuid

st.set_page_config(page_title="Grower Farm Tonnage Tracker", layout="wide")

st.title("Grower Farm Tonnage Tracker")

# -------------------------------------------------
# INITIALISE SESSION STATE
# -------------------------------------------------
if "growers" not in st.session_state:
    st.session_state.growers = []

# -------------------------------------------------
# ADD GROWER
# -------------------------------------------------
st.subheader("Add New Grower")
new_grower_name = st.text_input("Grower Name")

if st.button("Add Grower"):
    if new_grower_name.strip():

        st.session_state.growers.append({
            "id": str(uuid.uuid4()),
            "name": new_grower_name,
            "farms": []
        })

        st.rerun()

# -------------------------------------------------
# MAIN SECTION
# -------------------------------------------------
if st.session_state.growers:

    grower_names = [g["name"] for g in st.session_state.growers]
    selected_grower_name = st.selectbox("Select Grower", grower_names)

    grower = next(g for g in st.session_state.growers if g["name"] == selected_grower_name)
    grower_id = grower["id"]

    st.divider()
    st.subheader(f"Grower: {selected_grower_name}")

    # -------------------------------------------------
    # ADD FARM
    # -------------------------------------------------
    st.markdown("### Add Farm")
    new_farm_name = st.text_input("Farm Name")

    if st.button("Add Farm"):
        if new_farm_name.strip():

            farm_id = str(uuid.uuid4())

            grower["farms"].append({
                "id": farm_id,
                "name": new_farm_name
            })

            # initialise session keys safely
            st.session_state.setdefault(f"total_{farm_id}", 0.0)
            st.session_state.setdefault(f"cut_{farm_id}", 0.0)
            st.session_state.setdefault(f"tpb_{farm_id}", 0.0)

            st.rerun()

    # -------------------------------------------------
    # ALL FARMS VIEW
    # -------------------------------------------------
    if grower["farms"]:

        st.divider()
        st.subheader("Farm Summary")

        total_all = 0
        cut_all = 0
        weighted_tpb_total = 0

        header = st.columns(6)
        header[0].write("**Farm**")
        header[1].write("**Total Tonnes**")
        header[2].write("**Tonnes Cut**")
        header[3].write("**Remaining**")
        header[4].write("**% Cut**")
        header[5].write("**Tonnes / Bin**")

        for farm in grower["farms"]:

            farm_id = farm["id"]

            st.session_state.setdefault(f"total_{farm_id}", 0.0)
            st.session_state.setdefault(f"cut_{farm_id}", 0.0)
            st.session_state.setdefault(f"tpb_{farm_id}", 0.0)

            total = st.session_state[f"total_{farm_id}"]
            cut = st.session_state[f"cut_{farm_id}"]
            tpb = st.session_state[f"tpb_{farm_id}"]

            remaining = total - cut
            percent_cut = (cut / total * 100) if total > 0 else 0

            row = st.columns(6)

            row[0].write(farm["name"])

            row[1].number_input(
                "",
                min_value=0.0,
                key=f"total_{farm_id}"
            )

            row[2].number_input(
                "",
                min_value=0.0,
                key=f"cut_{farm_id}"
            )

            row[3].write(f"{remaining:.2f}")
            row[4].write(f"{percent_cut:.2f}%")

            row[5].number_input(
                "",
                min_value=0.0,
                key=f"tpb_{farm_id}"
            )

            total_all += total
            cut_all += cut
            weighted_tpb_total += total * tpb

        st.divider()

        remaining_all = total_all - cut_all
        percent_all = (cut_all / total_all * 100) if total_all > 0 else 0
        average_tpb = (weighted_tpb_total / total_all) if total_all > 0 else 0

        total_row = st.columns(6)
        total_row[0].write("**TOTAL**")
        total_row[1].write(f"**{total_all:.2f}**")
        total_row[2].write(f"**{cut_all:.2f}**")
        total_row[3].write(f"**{remaining_all:.2f}**")
        total_row[4].write(f"**{percent_all:.2f}%**")
        total_row[5].write(f"**{average_tpb:.2f}**")

        # -------------------------------------------------
        # GROWER TARGET SECTION (OPTION A)
        # -------------------------------------------------
        st.divider()
        st.subheader("Grower Target Planning")

        grower_target_percent = st.number_input(
            "Grower Target %",
            min_value=0.0,
            max_value=200.0,
            value=100.0,
            step=1.0,
            key=f"grower_target_{grower_id}"
        )

        days_remaining = st.number_input(
            "Days Remaining",
            min_value=1,
            value=7,
            step=1,
            key=f"grower_days_{grower_id}"
        )

        target_tonnes = total_all * (grower_target_percent / 100)
        tonnes_needed = max(target_tonnes - cut_all, 0)

        bins_required = tonnes_needed / average_tpb if average_tpb > 0 else 0
        bins_per_day_required = bins_required / days_remaining if days_remaining > 0 else 0

        st.markdown("### Target Requirements")

        colA, colB, colC = st.columns(3)

        colA.metric("Target Tonnes", f"{target_tonnes:.2f}")
        colB.metric("Tonnes Required", f"{tonnes_needed:.2f}")
        colC.metric("Bins Per Day Required", f"{bins_per_day_required:.2f}")

    else:
        st.info("No farms added for this grower yet.")

else:
    st.info("No growers added yet.")
