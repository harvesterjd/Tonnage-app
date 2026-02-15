import streamlit as st
import uuid
import json
import os
import math

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Grower Dashboard", layout="wide")
st.title("🌾 Grower Production Dashboard")

DATA_FILE = "data.json"


# -------------------------------------------------
# DATA HANDLING
# -------------------------------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.growers, f, indent=4)


# -------------------------------------------------
# INITIALIZE STATE
# -------------------------------------------------
if "growers" not in st.session_state:
    st.session_state.growers = load_data()


# -------------------------------------------------
# CALLBACK FUNCTIONS
# -------------------------------------------------
def add_day(farm_id, grower):
    step = grower["bin_weight"] * grower["bins_per_day"]
    cut_key = f"cut_{farm_id}"
    total_key = f"total_{farm_id}"

    if step > 0:
        st.session_state[cut_key] = min(
            st.session_state[cut_key] + step,
            st.session_state[total_key]
        )


def remove_day(farm_id, grower):
    step = grower["bin_weight"] * grower["bins_per_day"]
    cut_key = f"cut_{farm_id}"

    if step > 0:
        st.session_state[cut_key] = max(
            st.session_state[cut_key] - step,
            0
        )


# -------------------------------------------------
# ADD GROWER
# -------------------------------------------------
with st.container():
    st.subheader("Add Grower")

    col1, col2 = st.columns([3, 1])

    with col1:
        new_grower = st.text_input("Grower Name")

    with col2:
        if st.button("Add"):
            if new_grower.strip():
                st.session_state.growers.append({
                    "id": str(uuid.uuid4()),
                    "name": new_grower,
                    "farms": [],
                    "target_percent": 0.0,
                    "bin_weight": 0.0,
                    "bins_per_day": 0.0
                })
                save_data()
                st.rerun()


# -------------------------------------------------
# SELECT GROWER
# -------------------------------------------------
if st.session_state.growers:

    grower_names = [g["name"] for g in st.session_state.growers]
    selected_name = st.selectbox("Select Grower", grower_names)

    grower = next(g for g in st.session_state.growers if g["name"] == selected_name)

    st.divider()

    # -------------------------------------------------
    # SETTINGS ROW
    # -------------------------------------------------
    st.subheader("Production Settings")

    s1, s2, s3 = st.columns(3)

    grower["target_percent"] = s1.number_input(
        "Target %",
        0.0, 100.0,
        value=float(grower["target_percent"])
    )

    grower["bin_weight"] = s2.number_input(
        "Tonnes per Bin",
        0.0,
        value=float(grower["bin_weight"])
    )

    grower["bins_per_day"] = s3.number_input(
        "Bins per Day",
        0.0,
        value=float(grower["bins_per_day"])
    )

    save_data()

    st.divider()

    # -------------------------------------------------
    # ADD FARM
    # -------------------------------------------------
    st.subheader("Add Farm")

    f1, f2 = st.columns([3, 1])

    with f1:
        new_farm = st.text_input("Farm Name")

    with f2:
        if st.button("Add Farm"):
            if new_farm.strip():
                grower["farms"].append({
                    "id": str(uuid.uuid4()),
                    "name": new_farm,
                    "total": 0.0,
                    "cut": 0.0
                })
                save_data()
                st.rerun()

    st.divider()

    # -------------------------------------------------
    # FARMS TABLE
    # -------------------------------------------------
    if grower["farms"]:

        total_all = 0
        cut_all = 0

        for farm in grower["farms"]:

            total_key = f"total_{farm['id']}"
            cut_key = f"cut_{farm['id']}"

            if total_key not in st.session_state:
                st.session_state[total_key] = farm["total"]

            if cut_key not in st.session_state:
                st.session_state[cut_key] = farm["cut"]

            st.markdown(f"### 🏡 {farm['name']}")

            c1, c2, c3, c4 = st.columns([2, 2, 2, 1])

            with c1:
                st.number_input("Total Tonnes", 0.0, key=total_key)

            with c2:
                st.number_input(
                    "Tonnes Cut",
                    0.0,
                    st.session_state[total_key],
                    key=cut_key
                )

            with c3:
                st.button(
                    "➕ Add Day",
                    key=f"plus_{farm['id']}",
                    on_click=add_day,
                    args=(farm["id"], grower)
                )

                st.button(
                    "➖ Remove Day",
                    key=f"minus_{farm['id']}",
                    on_click=remove_day,
                    args=(farm["id"], grower)
                )

            with c4:
                if st.button("🗑", key=f"delete_{farm['id']}"):
                    grower["farms"] = [
                        f for f in grower["farms"]
                        if f["id"] != farm["id"]
                    ]
                    save_data()
                    st.rerun()

            # Update data
            farm["total"] = st.session_state[total_key]
            farm["cut"] = st.session_state[cut_key]

            percent = (
                farm["cut"] / farm["total"] * 100
                if farm["total"] > 0 else 0
            )

            st.progress(percent / 100)
            st.caption(f"{percent:.1f}% Complete")

            total_all += farm["total"]
            cut_all += farm["cut"]

            st.divider()

        # -------------------------------------------------
        # DASHBOARD METRICS
        # -------------------------------------------------
        st.subheader("📊 Grower Overview")

        percent_total = (cut_all / total_all * 100) if total_all > 0 else 0
        target_tonnes = total_all * grower["target_percent"] / 100
        remaining = max(target_tonnes - cut_all, 0)

        bins_required = (
            remaining / grower["bin_weight"]
            if grower["bin_weight"] > 0 else 0
        )

        days_required = (
            bins_required / grower["bins_per_day"]
            if grower["bins_per_day"] > 0 else 0
        )

        m1, m2, m3, m4 = st.columns(4)

        m1.metric("Total Tonnes", f"{total_all:.2f}")
        m2.metric("Total Cut", f"{cut_all:.2f}")
        m3.metric("% Complete", f"{percent_total:.1f}%")
        m4.metric("Days to Target", math.ceil(days_required) if days_required > 0 else 0)

else:
    st.info("Add a grower to begin.")
