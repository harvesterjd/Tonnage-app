import streamlit as st
import math

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

            # --- Basic Inputs ---
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

            st.divider()

            # --- Production Inputs ---
            tonnes_per_bin = st.number_input(
                "Tonnes per Bin",
                min_value=0.0,
                value=0.0,
                key=f"tpb_{i}"
            )

            bins_per_day = st.number_input(
                "Bins per Day",
                min_value=0.0,
                value=0.0,
                key=f"bpd_{i}"
            )

            # ---------------- Add One Day Production ----------------
            if st.button("Add One Day Production", key=f"add_day_{i}"):

                daily_tonnes = bins_per_day * tonnes_per_bin
                new_cut = farm.get("cut", 0.0) + daily_tonnes

                # Prevent exceeding total
                if new_cut > total:
                    new_cut = total

                farm["cut"] = new_cut
                st.success(f"Added {daily_tonnes:.2f} tonnes to cut total.")
                st.rerun()

            st.divider()

            # --- Day Projection Tool ---
            days_planned = st.number_input(
                "Days Planned (Projection)",
                min_value=0,
                value=0,
                step=1,
                key=f"days_{i}"
            )

            # ---------------- Current Calculations ----------------
            remaining = total - cut
            percent_cut = (cut / total * 100) if total > 0 else 0

            target_tonnes = (total * target_percent / 100)
            tonnes_needed = max(target_tonnes - cut, 0)

            bins_required = (tonnes_needed / tonnes_per_bin) if tonnes_per_bin > 0 else 0
            days_required = (bins_required / bins_per_day) if bins_per_day > 0 else 0

            # ---------------- Projection Calculations ----------------
            projected_bins = bins_per_day * days_planned
            projected_tonnes = projected_bins * tonnes_per_bin
            projected_total_cut = min(cut + projected_tonnes, total)

            projected_percent = (projected_total_cut / total * 100) if total > 0 else 0

            # ---------------- Display ----------------
            st.write(f"Tonnes Remaining: {remaining:.2f}")
            st.write(f"% Cut: {percent_cut:.2f}%")

            st.divider()

            st.write(f"Target Tonnes ({target_percent}%): {target_tonnes:.2f}")
            st.write(f"Tonnes Required to Reach Target: {tonnes_needed:.2f}")
            st.write(f"Bins Required: {math.ceil(bins_required) if bins_required > 0 else 0}")
            st.write(f"Days Required: {days_required:.2f}")

            st.divider()

            st.subheader("Projection Based on Days")
            st.write(f"Projected Additional Tonnes: {projected_tonnes:.2f}")
            st.write(f"Projected Total Cut: {projected_total_cut:.2f}")
            st.write(f"Projected % Cut: {projected_percent:.2f}%")

            # --- Save updates ---
            farm["total"] = total
            farm["cut"] = cut
            farm["target_percent"] = target_percent

            st.divider()

            # --- Delete Farm ---
            if st.button("Delete This Farm", key=f"delete_{i}"):
                st.session_state.farms.pop(i)
                st.rerun()

else:
    st.info("No farms added yet.")
