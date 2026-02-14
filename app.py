import streamlit as st

st.title("Farm Tonnage Tracker")

# -----------------------------
# 1️⃣ Initialize session state safely
# -----------------------------
if "farms" not in st.session_state:
    st.session_state.farms = []

if not isinstance(st.session_state.farms, list):
    st.session_state.farms = []

# -----------------------------
# 2️⃣ Add new farm
# -----------------------------
st.subheader("Add New Farm")

new_farm_name = st.text_input("Farm Number")

if st.button("Add Farm"):
    if new_farm_name.strip() != "":
        st.session_state.farms.append({
            "name": new_farm_name,
            "total": 0.0,
            "cut": 0.0
        })
        st.success(f"Farm {new_farm_name} added!")
        st.rerun()

# -----------------------------
# 3️⃣ Display farms
# -----------------------------
valid_farms = [
    farm for farm in st.session_state.farms
    if isinstance(farm, dict) and "name" in farm
]

if len(valid_farms) > 0:

    tabs = st.tabs([farm["name"] for farm in valid_farms])

    for i, farm in enumerate(valid_farms):

        with tabs[i]:

            st.subheader(f"Farm {farm['name']}")

            total = st.number_input(
                "Total Tonnes",
                min_value=0.0,
                value=farm.get("total", 0.0),
                key=f"total_{i}"
            )

            cut = st.number_input(
                "Tonnes Cut",
                min_value=0.0,
                value=farm.get("cut", 0.0),
                key=f"cut_{i}"
            )

            remaining = total - cut
            percent_cut = (cut / total * 100) if total > 0 else 0

            st.write(f"Tonnes Remaining: {remaining}")
            st.write(f"% Cut: {percent_cut:.2f}%")

            # Save updates
            farm["total"] = total
            farm["cut"] = cut

            st.divider()

            # 🔴 Delete Button
            if st.button("Delete This Farm", key=f"delete_{i}"):
                st.session_state.farms.pop(i)
                st.rerun()

else:
    st.info("No farms added yet.")
