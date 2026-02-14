import streamlit as st

st.set_page_config(page_title="Grower Tonnage App", layout="wide")

st.title("Grower Tonnage Management")

# -----------------------------
# SESSION STATE INITIALISE
# -----------------------------
if "growers" not in st.session_state:
    st.session_state.growers = []

# -----------------------------
# ADD GROWER SECTION
# -----------------------------
st.subheader("Add New Grower")

col1, col2 = st.columns(2)

with col1:
    new_grower_name = st.text_input("Grower Name")

with col2:
    new_farms_input = st.text_input("Farm Numbers (comma separated)")

if st.button("Add Grower"):

    if new_grower_name:

        farm_list = []
        if new_farms_input:
            farms = [f.strip() for f in new_farms_input.split(",")]

            for farm in farms:
                farm_list.append({
                    "id": f"{new_grower_name}_{farm}",
                    "name": farm
                })

        st.session_state.growers.append({
            "name": new_grower_name,
            "farms": farm_list
        })

        st.success("Grower Added")
        st.rerun()

# -----------------------------
# SELECT GROWER
# -----------------------------
if st.session_state.growers:

    st.subheader("Select Grower")

    grower_names = [g["name"] for g in st.session_state.growers]

    selected_name = st.selectbox("Choose Grower", grower_names)

    grower = next(g for g in st.session_state.growers if g["name"] == selected_name)

    # -----------------------------
    # DELETE GROWER
    # -----------------------------
    if st.button("Delete Grower"):
        st.session_state.growers = [
            g for g in st.session_state.growers if g["name"] != selected_name
        ]
        st.success("Grower Deleted")
        st.rerun()

    # -----------------------------
    # ADD FARM TO GROWER
    # -----------------------------
    st.subheader("Add Farm to Grower")

    new_farm = st.text_input("New Farm Number")

    if st.button("Add Farm"):

        if new_farm:

            grower["farms"].append({
                "id": f"{selected_name}_{new_farm}",
                "name": new_farm
            })

            st.success("Farm Added")
            st.rerun()

    # -----------------------------
    # FARM PRODUCTION TABLE
    # -----------------------------
    st.subheader("Grower Farm Production")

    if grower["farms"]:

        total_all = 0
        cut_all = 0

        # Header row
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        col1.write("**Farm**")
        col2.write("**Total Tonnes**")
        col3.write("**Add Today**")
        col4.write("**Add Btn**")
        col5.write("**Tonnes Cut**")
        col6.write("**Tonnes Rem**")
        col7.write("**% Cut**")

        for farm in grower["farms"]:

            farm_id = farm["id"]

            # Initialise session state
            if f"total_{farm_id}" not in st.session_state:
                st.session_state[f"total_{farm_id}"] = 0.0

            if f"cut_{farm_id}" not in st.session_state:
                st.session_state[f"cut_{farm_id}"] = 0.0

            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

            col1.write(farm["name"])

            # Editable total
            total = col2.number_input(
                "",
                value=st.session_state[f"total_{farm_id}"],
                key=f"total_input_{farm_id}"
            )

            st.session_state[f"total_{farm_id}"] = total

            # Daily input
            today = col3.number_input(
                "",
                value=0.0,
                key=f"today_{farm_id}"
            )

            # Add button
            if col4.button("Add", key=f"add_{farm_id}"):

                st.session_state[f"cut_{farm_id}"] += today
                st.session_state[f"today_{farm_id}"] = 0.0
                st.rerun()

            cut = st.session_state[f"cut_{farm_id}"]
            remaining = total - cut
            percent = (cut / total * 100) if total > 0 else 0

            col5.write(f"{cut:.2f}")
            col6.write(f"{remaining:.2f}")
            col7.write(f"{percent:.0f}%")

            # Delete farm button
            if col1.button("❌", key=f"delete_{farm_id}"):

                grower["farms"] = [
                    f for f in grower["farms"] if f["id"] != farm_id
                ]

                # Clean session state
                for key in list(st.session_state.keys()):
                    if farm_id in key:
                        del st.session_state[key]

                st.rerun()

            total_all += total
            cut_all += cut

        # -----------------------------
        # TOTAL ROW
        # -----------------------------
        st.divider()

        remaining_all = total_all - cut_all
        percent_all = (cut_all / total_all * 100) if total_all > 0 else 0

        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

        col1.write("**Total All Farms**")
        col2.write(f"**{total_all:.2f}**")
        col3.write("")
        col4.write("")
        col5.write(f"**{cut_all:.2f}**")
        col6.write(f"**{remaining_all:.2f}**")
        col7.write(f"**{percent_all:.0f}%**")

else:
    st.info("Add a grower to begin.")
