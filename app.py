import streamlit as st

st.set_page_config(page_title="Tonnage Tracker", layout="wide")

st.title("🚜 Farm Tonnage Tracker")

# -----------------------------
# SESSION STATE INITIALISATION
# -----------------------------

if "farms" not in st.session_state:
    st.session_state.farms = []

if "tonnes_per_bin" not in st.session_state:
    st.session_state.tonnes_per_bin = 10.0


# -----------------------------
# SIDEBAR – DAILY PRODUCTION
# -----------------------------

st.sidebar.header("📦 Daily Production")

tonnes_per_bin = st.sidebar.number_input(
    "Tonnes per Bin",
    min_value=0.0,
    value=st.session_state.tonnes_per_bin,
    step=0.5,
)

bins_today = st.sidebar.number_input(
    "Bins Filled Today",
    min_value=0,
    value=0,
    step=1,
)

daily_tonnes = bins_today * tonnes_per_bin

st.sidebar.write(f"Tonnes Today: {daily_tonnes:.2f}")

if len(st.session_state.farms) > 0:

    farm_names = [farm["name"] for farm in st.session_state.farms]

    selected_farm_name = st.sidebar.selectbox(
        "Select Farm",
        farm_names
    )

    if st.sidebar.button("➕ Add One Day Production"):
        for farm in st.session_state.farms:
            if farm["name"] == selected_farm_name:
                farm["tonnes_cut"] += daily_tonnes
                break
        st.rerun()


# -----------------------------
# ADD FARM SECTION
# -----------------------------

st.subheader("➕ Add New Farm")

col1, col2, col3 = st.columns(3)

with col1:
    farm_name = st.text_input("Farm Name")

with col2:
    total_tonnes = st.number_input("Total Tonnes", min_value=0.0, value=0.0)

with col3:
    target_percent = st.number_input("Target %", min_value=0.0, max_value=100.0, value=100.0)

if st.button("Add Farm"):
    if farm_name:
        st.session_state.farms.append({
            "name": farm_name,
            "total": total_tonnes,
            "target_percent": target_percent,
            "tonnes_cut": 0.0
        })
        st.rerun()


# -----------------------------
# FARM DISPLAY SECTION
# -----------------------------

st.subheader("📊 Farm Progress")

for i, farm in enumerate(st.session_state.farms):

    st.markdown("---")
    st.subheader(farm["name"])

    # Ensure safe defaults
    if "tonnes_cut" not in farm:
        farm["tonnes_cut"] = 0.0
    if "target_percent" not in farm:
        farm["target_percent"] = 100.0

    # -----------------------------
    # CALCULATIONS
    # -----------------------------

    target_tonnes = farm["total"] * farm["target_percent"] / 100
    remaining_tonnes = max(target_tonnes - farm["tonnes_cut"], 0)

    bins_required = remaining_tonnes / tonnes_per_bin if tonnes_per_bin > 0 else 0
    days_required = bins_required / bins_today if bins_today > 0 else 0

    # -----------------------------
    # DISPLAY
    # -----------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write(f"Total Tonnes: {farm['total']:.2f}")

    with col2:
        st.write(f"Target Tonnes: {target_tonnes:.2f}")

    with col3:
        st.write(f"Tonnes Cut: {farm['tonnes_cut']:.2f}")

    with col4:
        st.write(f"Remaining: {remaining_tonnes:.2f}")

    progress = farm["tonnes_cut"] / target_tonnes if target_tonnes > 0 else 0
    st.progress(min(progress, 1.0))

    # Extra Calculations
    col5, col6 = st.columns(2)

    with col5:
        st.write(f"Bins Required: {bins_required:.1f}")

    with col6:
        if bins_today > 0:
            st.write(f"Days Required: {days_required:.1f}")
        else:
            st.write("Days Required: -")

    # Delete
    if st.button(f"❌ Delete {farm['name']}", key=f"delete_{i}"):
        st.session_state.farms.pop(i)
        st.rerun()
