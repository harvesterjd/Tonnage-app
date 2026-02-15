import streamlit as st

st.set_page_config(page_title="Grower Tonnage Tracker", layout="wide")

st.title("Grower Tonnage Tracker")

# -----------------------------
# Sample Grower Data Structure
# -----------------------------

if "growers" not in st.session_state:
    st.session_state.growers = {
        1: {
            "name": "Smith Farms",
            "farms": {
                101: {"name": "North Block", "tonnes": 0.0},
                102: {"name": "River Block", "tonnes": 0.0},
                103: {"name": "Hill Block", "tonnes": 0.0},
            },
        }
    }

# -----------------------------
# Select Grower
# -----------------------------

grower_options = {
    grower_id: data["name"]
    for grower_id, data in st.session_state.growers.items()
}

selected_grower_id = st.selectbox(
    "Select Grower",
    options=list(grower_options.keys()),
    format_func=lambda x: grower_options[x],
)

grower = st.session_state.growers[selected_grower_id]

st.subheader(f"Grower: {grower['name']}")

# -----------------------------
# Grower Target Section
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    total_target = st.number_input(
        "Grower Total Target (tonnes)",
        min_value=0.0,
        value=1000.0,
        step=50.0,
    )

with col2:
    target_percent = st.number_input(
        "Target % to Cut",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=5.0,
    )

adjusted_target = total_target * (target_percent / 100)

st.info(f"Adjusted Target Tonnes: {adjusted_target:.2f} t")

days_remaining = st.number_input(
    "Days Remaining",
    min_value=1,
    value=10,
    step=1,
)

# -------------------------------------------------
# ALL FARMS VIEW
# -------------------------------------------------

if grower["farms"]:

    st.subheader("Farm Summary")

    total_all = 0
    cut_all = 0
    weighted_tpb_total = 0

    header = st.columns(6)
    header[0].write("**Farm**")
    header[1].write("**Total**")
    header[2].write("**Cut**")
    header[3].write("**Remaining**")
    header[4].write("**% Cut**")
    header[5].write("**TPB**")

    for farm in grower["farms"]:

        farm_id = farm["id"]

        total = st.session_state.get(f"total_{farm_id}", 0.0)
        cut = st.session_state.get(f"cut_{farm_id}", 0.0)
        tpb = st.session_state.get(f"tpb_{farm_id}", 0.0)

        remaining = total - cut
        percent_cut = (cut / total * 100) if total > 0 else 0

        row = st.columns(6)
        row[0].write(farm["name"])
        row[1].write(f"{total:.2f}")
        row[2].write(f"{cut:.2f}")
        row[3].write(f"{remaining:.2f}")
        row[4].write(f"{percent_cut:.2f}%")
        row[5].write(f"{tpb:.2f}")

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
    # GROWER TARGET SECTION
    # -------------------------------------------------

    st.divider()
    st.subheader("Grower Target Planning")

    grower_target = st.number_input(
        "Grower Target %",
        min_value=0.0,
        max_value=100.0,
        key=f"grower_target_{grower_id}"
    )

    days_remaining = st.number_input(
        "Days Remaining",
        min_value=1,
        step=1,
        key=f"grower_days_{grower_id}"
    )

    target_tonnes = total_all * grower_target / 100
    tonnes_needed = max(target_tonnes - cut_all, 0)

    bins_required = tonnes_needed / average_tpb if average_tpb > 0 else 0
    bins_per_day_required = bins_required / days_remaining if days_remaining > 0 else 0

    st.write(f"Target Tonnes: {target_tonnes:.2f}")
    st.write(f"Tonnes Required: {tonnes_needed:.2f}")
    st.write(f"Bins Required: {math.ceil(bins_required) if bins_required > 0 else 0}")
    st.write(f"Bins Per Day Required: {bins_per_day_required:.2f}")

else:
    st.info("No farms added for this grower yet.")

# -----------------------------
# Combined Totals Row
# -----------------------------

st.markdown("---")
st.subheader("Combined Total")

st.write(f"Total Tonnes Delivered: {total_current_tonnes:.2f} t")

remaining_to_cut = max(adjusted_target - total_current_tonnes, 0)

st.write(f"Tonnes Remaining to Cut: {remaining_to_cut:.2f} t")

bins_per_day = remaining_to_cut / days_remaining

st.success(f"Required Tonnes per Day: {bins_per_day:.2f} t/day")
