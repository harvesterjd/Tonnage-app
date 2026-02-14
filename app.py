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
# GLOBAL SETTINGS
# -----------------------------

st.sidebar.header("⚙️ Settings")

st.session_state.tonnes_per_bin = st.sidebar.number_input(
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

daily_tonnes = bins_today * st.session_state.tonnes_per_bin

if st.sidebar.button("➕ Add One Day Production To Selected Farm"):
    selected_index = st.sidebar.selectbox(
        "Select Farm",
        range(len(st.session_state.farms)),
        format_func=lambda x: st.session_state.farms[x]["name"] if st.session_state.farms else "",
    )

    if st.session_state.farms:
        st.session_state.farms[selected_index]["tonnes_cut"] += daily_tonnes
        st.success("Production added successfully!")


# -----------------------------
# ADD FARM
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
        st.success("Farm added!")


# -----------------------------
# DISPLAY FARMS
# -----------------------------

st.subheader("📊 Farm Progress")

for i, farm in enumerate(st.session_state.farms):

    st.markdown("---")
    st.subheader(farm["name"])

    target_tonnes = (farm["total"] * farm["target_percent"] / 100)
    remaining = max(target_tonnes - farm["tonnes_cut"], 0)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(f"Total Tonnes: {farm['total']}")

    with col2:
        st.write(f"Target Tonnes: {target_tonnes:.2f}")

    with col3:
        st.write(f"Tonnes Cut: {farm['tonnes_cut']:.2f}")

    st.progress(
        farm["tonnes_cut"] / target_tonnes if target_tonnes > 0 else 0
    )

    st.write(f"Remaining Tonnes: {remaining:.2f}")

    # Delete button
    if st.button(f"❌ Delete {farm['name']}", key=f"delete_{i}"):
        st.session_state.farms.pop(i)
        st.experimental_rerun()
