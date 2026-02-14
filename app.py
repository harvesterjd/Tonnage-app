import streamlit as st
import uuid

st.set_page_config(page_title="Grower Tonnage Manager", layout="wide")

st.title("Grower Tonnage Management")

# -------------------------------------------------
# INITIALISE SESSION STATE
# -------------------------------------------------
if "growers" not in st.session_state:
    st.session_state.growers = []

# -------------------------------------------------
# ADD NEW GROWER
# -------------------------------------------------
st.subheader("Add New Grower")

col1, col2 = st.columns(2)

new_grower_name = col1.text_input("Grower Name")
new_farms_input = col2.text_input("Farm Numbers (comma separated)")

if st.button("Add Grower"):

    if new_grower_name.strip():

        grower_id = str(uuid.uuid4())

        farms = []
        if new_farms_input.strip():
            farm_numbers = [f.strip() for f in new_farms_input.split(",")]

            for farm_number in farm_numbers:
                farms.append({
                    "id": str(uuid.uuid4()),
                    "name": farm_number
                })

        st.session_state.growers.append({
            "id": grower_id,
            "name": new_grower_name,
            "farms": farms
        })

        st.rerun()

# -------------------------------------------------
# IF GROWERS EXIST
# -------------------------------------------------
if st.session_state.growers:

    st.divider()
    st.subheader("Select Grower")

    grower_names = [g["name"] for g in st.session_state.growers]

    selected_name = st.selectbox("Choose Grower", grower_names)

    grower = next(g for g in st.session_state.growers if g["name"] == selected_name)

    grower_id = grower["id"]

    # -------------------------------------------------
    # DELETE GROWER
    # -------------------------------------------------
    if st.button("Delete Grower"):

        st.session_state.growers = [
            g for g in st.session_state.growers
            if g["id"] != grower_id
        ]

        st.rerun()

    # -------------------------------------------------
    # ADD FARM
    # -------------------------------------------------
    st.subheader("Add Farm to Grower")

    new_farm = st.text_input("New Farm Number")

    if st.button("Add Farm"):

        if new_farm.strip():

            grower["farms"].append({
                "id": str(uuid.uuid4()),
                "name": new_farm
            })

            st.rerun()

    # -------------------------------------------------
    # FARM PRODUCTION TABLE
    # -------------------------------------------------
    st.divider()
    st.subheader("Grower Farm Production")

    if grower["farms"]:

        total_all = 0
        cut_all = 0

        header = st.columns(7)
        header[0].write("**Farm**")
        header[1].write("**Total Tonnes**")
        header[2].write("**Add Today**")
        header[3].write("**Add**")
        header[4].write("**Tonnes Cut**")
        header[5].write("**Remaining**")
        header[6].write("**% Cut**")

        for farm in grower["farms"]:

            farm_id = farm["id"]

            # Initialise farm session keys
            st.session_state.setdefault(f"total_{farm_id}", 0.0)
            st.session_state.setdefault(f"cut_{farm_id}", 0.0)

            cols = st.columns(7)

            cols[0].write(farm["name"])

            total = cols[1].number_input(
                "",
                min_value=0.0,
                value=st.session_state[f"total_{farm_id}"],
                key=f"total_{farm_id}"
            )

            today = cols[2].number_input(
                "",
                min_value=0.0,
                value=0.0,
                key=f"today_{farm_id}"
            )

            if cols[3].button("Add", key=f"add_{farm_id}"):

                st.session_state[f"cut_{farm_id}"] += today
                st.rerun()

            cut = st.session_state[f"cut_{farm_id}"]
            remaining = total - cut
            percent = (cut / total * 100) if total > 0 else 0

            cols[4].write(f"{cut:.2f}")
            cols[5].write(f"{remaining:.2f}")
            cols[6].write(f"{percent:.0f}%")

            # Delete farm
            if cols[0].button("❌", key=f"delete_{farm_id}"):

                grower["farms"] = [
                    f for f in grower["farms"]
                    if f["id"] != farm_id
                ]

                # Clean session state
                for key in list(st.session_state.keys()):
                    if farm_id in key:
                        del st.session_state[key]

                st.rerun()

            total_all += total
            cut_all += cut

        # -------------------------------------------------
        # TOTAL ROW
        # -------------------------------------------------
        st.divider()

        remaining_all = total_all - cut_all
        percent_all = (cut_all / total_all * 100) if total_all > 0 else 0

        total_row = st.columns(7)
        total_row[0].write("**TOTAL ALL FARMS**")
        total_row[1].write(f"**{total_all:.2f}**")
        total_row[2].write("")
        total_row[3].write("")
        total_row[4].write(f"**{cut_all:.2f}**")
        total_row[5].write(f"**{remaining_all:.2f}**")
        total_row[6].write(f"**{percent_all:.0f}%**")

    else:
        st.info("No farms added for this grower yet.")

else:
    st.info("Add a grower to begin.")
