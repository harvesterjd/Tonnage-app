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

# -----------------------------
# Farms Table
# -----------------------------

st.markdown("### Farms")

total_current_tonnes = 0.0

for farm_id, farm in grower["farms"].items():

    col1, col2 = st.columns(2)

    with col1:
        st.write(farm["name"])

    with col2:
        tonnes = st.number_input(
            "Tonnes",
            min_value=0.0,
            key=f"farm_{farm_id}",
            value=farm["tonnes"],
        )
        farm["tonnes"] = tonnes

    total_current_tonnes += farm["tonnes"]

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
