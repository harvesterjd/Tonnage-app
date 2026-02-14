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
            "cut": 0.0,
            "target_percent": 0.0
        })
        st.success(f"Farm {new_farm_name} added!")
        st.rerun()

# -----------------------------
# 3️⃣ Display farms
# -----------------------------
if len(st.session_state.farms) > 0:

    tabs = st.tabs([farm["name"] for farm in st.session_state.farms])

    for i, farm in enumerate(st.session_state.farms):

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

            target_percent = st.number_input(
                "Target %",
                min_value=0.0,
                max_value=100.0,
                value=farm.get("target_percent", 0.0),
                key=f"target_{i}"
            )

            # ---------------- Calculations ----------------
            remaining = total - cut
            percent_cut = (cut / total * 100) if total > 0 else 0

            target_tonnes = (total * target_percent / 100)
            tonnes_needed = target_tonnes - cut

            if tonnes_needed < 0:
                tonnes_needed = 0

            # ---------------- Display ----------------
            st.write(f"Tonnes Remaining: {remaining}")
            st.write(f"% Cut: {percent_cut:.2f}%")

            st.divider()

            st.write(f"Target Tonnes ({target_percent}%): {target_tonnes:.2f}")
            st.write(f"Tonnes Required to Reach Target: {tonnes_needed:.2f}")

            # Save updates
            farm["total"] = total
            farm["cut"] = cut
            farm["target_percent"] = target_percent

            st.divider()

            # Delete Button
            if st.button("Delete This Farm", key=f"delete_{i}"):
                st.session_state.farms.pop(i)
                st.rerun()

else:
    st.info("No farms added yet.")
