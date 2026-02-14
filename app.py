import streamlit as st

st.title("Farm Tonnage Tracker")

# -----------------------------
# 1️⃣ Initialize session state
# -----------------------------
if "farms" not in st.session_state:
    st.session_state.farms = []

# -----------------------------
# 2️⃣ Add new farm section
# -----------------------------
st.subheader("Add New Farm")

new_farm_name = st.text_input("Farm Number")

if st.button("Add Farm"):
    if new_farm_name != "":
        st.session_state.farms.append({
            "name": new_farm_name,
            "total": 0.0,
            "cut": 0.0
        })
        st.success(f"Farm {new_farm_name} added!")

# -----------------------------
# 3️⃣ Show farms in tabs
# -----------------------------
if len(st.session_state.farms) > 0:

    tabs = st.tabs([farm["name"] for farm in st.session_state.farms])

    for i, farm in enumerate(st.session_state.farms):

        with tabs[i]:

            st.subheader(f"Farm {farm['name']}")

            total = st.number_input(
                "Total Tonnes",
                min_value=0.0,
                value=farm["total"],
                key=f"total_{i}"
            )

            cut = st.number_input(
                "Tonnes Cut",
                min_value=0.0,
                value=farm["cut"],
                key=f"cut_{i}"
            )

            remaining = total - cut

            if total > 0:
                percent_cut = (cut / total) * 100
            else:
                percent_cut = 0

            st.write(f"Tonnes Remaining: {remaining}")
            st.write(f"% Cut: {percent_cut:.2f}%")

            # Save updated values
            st.session_state.farms[i]["total"] = total
            st.session_state.farms[i]["cut"] = cut

else:
    st.info("No farms added yet.")
