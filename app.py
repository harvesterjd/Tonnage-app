import streamlit as st
from datetime import date

st.set_page_config(page_title="Tonnage Tracker", layout="wide")

# ----------------------------
# SESSION STATE INITIALISATION
# ----------------------------
if "growers" not in st.session_state:
    st.session_state.growers = {}

# ----------------------------
# ADD GROWER
# ----------------------------
st.header("Add Grower")

with st.form("add_grower"):
    new_grower = st.text_input("Grower Name")
    grower_target = st.number_input("Grower Target (Tonnes)", min_value=0.0, step=1.0)
    end_date = st.date_input("Season End Date")
    submit_grower = st.form_submit_button("Add Grower")

    if submit_grower and new_grower:
        st.session_state.growers[new_grower] = {
            "target": grower_target,
            "end_date": end_date,
            "farms": {}
        }

# ----------------------------
# DISPLAY GROWERS
# ----------------------------
st.header("Growers")

for grower_name, grower_data in st.session_state.growers.items():

    st.subheader(f"{grower_name}")

    grower_target = grower_data["target"]
    end_date = grower_data["end_date"]
    farms = grower_data["farms"]

    # ----------------------------
    # DAYS REMAINING (Grower Level)
    # ----------------------------
    days_remaining = (end_date - date.today()).days
    days_remaining = max(days_remaining, 0)

    st.write(f"Target: {grower_target} T")
    st.write(f"Days Remaining: {days_remaining}")

    # ----------------------------
    # ADD FARM
    # ----------------------------
    with st.form(f"add_farm_{grower_name}"):
        farm_name = st.text_input("Farm Name", key=f"farm_{grower_name}")
        submit_farm = st.form_submit_button("Add Farm")

        if submit_farm and farm_name:
            farms[farm_name] = {
                "actual": 0.0
            }

    # ----------------------------
    # FARM TABLE
    # ----------------------------
    total_actual = 0

    for farm_name, farm_data in list(farms.items()):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write(farm_name)

        with col2:
            farm_data["actual"] = st.number_input(
                "Actual Tonnes",
                value=farm_data["actual"],
                step=1.0,
                key=f"{grower_name}_{farm_name}"
            )

        with col3:
            percent = (
                (farm_data["actual"] / grower_target) * 100
                if grower_target > 0 else 0
            )
            st.write(f"{percent:.1f}% of Grower Target")

        with col4:
            if st.button("Delete Farm", key=f"del_{grower_name}_{farm_name}"):
                del farms[farm_name]
                st.rerun()

        total_actual += farm_data["actual"]

    # ----------------------------
    # GROWER TOTALS
    # ----------------------------
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Total Actual**")

    with col2:
        st.write(f"**{total_actual:.1f} T**")

    with col3:
        total_percent = (
            (total_actual / grower_target) * 100
            if grower_target > 0 else 0
        )
        st.write(f"**{total_percent:.1f}% of Target**")

    st.markdown("------")
