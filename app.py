import streamlit as st
import math

st.title("Farm Tonnage Tracker")

# -----------------------------
# Initialize
# -----------------------------
if "farms" not in st.session_state:
    st.session_state.farms = []

# -----------------------------
# Add Farm
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
        st.rerun()

# -----------------------------
# Display Farms
# -----------------------------
if st.session_state.farms:

    tabs = st.tabs([farm["name"] for farm in st.session_state.farms])

    for i, farm in enumerate(st.session_state.farms):

        with tabs[i]:

            st.subheader(f"Farm {farm['name']}")

            # ---------------- Total Tonnes ----------------
            total = st.number_input(
                "Total Tonnes",
                min_value=0.0,
                value=farm["total"],
                key=f"total_{i}"
            )

            # ---------------- Tonnes Cut (TRUE SESSION CONTROL) ----------------
            if f"cut_{i}" not in st.session_state:
                st.session_state[f"cut_{i}"] = farm["cut"]

            cut = st.number_input(
                "Tonnes Cut",
                min_value=0.0,
                key=f"cut_{i}"
            )

            # Keep farm synced
            farm["cut"] = st.session_state[f"cut_{i}"]

            # ---------------- Target ----------------
            target_percent = st.number_input(
                "Target %",
                min_value=0.0,
                max_value=100.0,
                value=farm["target_percent"],
                key=f"target_{i}"
            )

            st.divider()

            # ---------------- Production Inputs ----------------
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

                st.session_state[f"cut_{i}"] += daily_tonnes

                # Cap at total
                if st.session_state[f"cut_{i}"] > total:
                    st.session_state[f"cut_{i}"] = total

                st.rerun()

            st.divider()

            # ---------------- Calculations ----------------
            cut = st.session_state[f"cut_{i}"]

            remaining = total - cut
            percent_cut = (cut / total * 100) if total > 0 else 0

            target_tonnes = total * target_percent / 100
            tonnes_needed = max(target_tonnes - cut, 0)

            bins_required = (
                tonnes_needed / tonnes_per_bin
                if tonnes_per_bin > 0 else 0
            )

            days_required = (
                bins_required / bins_per_day
                if bins_per_day > 0 else 0
            )

            # ---------------- Display ----------------
            st.write(f"Tonnes Remaining: {remaining:.2f}")
            st.write(f"% Cut: {percent_cut:.2f}%")

            st.divider()

            st.write(f"Target Tonnes ({target_percent}%): {target_tonnes:.2f}")
            st.write(f"Tonnes Required to Reach Target: {tonnes_needed:.2f}")
            st.write(f"Bins Required: {math.ceil(bins_required) if bins_required > 0 else 0}")
            st.write(f"Days Required: {days_required:.2f}")

            # Save farm state
            farm["total"] = total
            farm["target_percent"] = target_percent
            farm["cut"] = st.session_state[f"cut_{i}"]

            st.session_state.farms[i] = farm

            st.divider()

            # ---------------- Delete ----------------
            if st.button("Delete This Farm", key=f"delete_{i}"):
                st.session_state.farms.pop(i)
                st.rerun()

else:
    st.info("No farms added yet.")
