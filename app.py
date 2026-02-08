 import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tonnage Planning Tool", layout="wide")

st.title("Tonnage Reduction & Bin Planning")

# ----------------------
# Global inputs
# ----------------------
col1, col2, col3 = st.columns(3)

with col1:
    target_percent = st.number_input(
        "Target % to remove",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        step=0.1
    )

with col2:
    bin_weight = st.number_input(
        "Bin weight (tons per bin)",
        min_value=0.0,
        value=1.0,
        step=0.1
    )

with col3:
    bins_per_day = st.number_input(
        "Bins allocated per day",
        min_value=0.0,
        value=10.0,
        step=1.0
    )

st.markdown("---")

# ----------------------
# Farm table (with editable Tons cut)
# ----------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Farm No": ["Farm 1"],
        "Tons": [0.0],
        "Tons cut": [0.0]
    })

edited_df = st.data_editor(
    st.session_state.data,
    num_rows="dynamic",
    use_container_width=True
)

df = edited_df.copy()

# ----------------------
# Apply default % where Tons cut not manually set
# ----------------------
default_cut = df["Tons"] * (target_percent / 100)

df["Tons cut"] = df["Tons cut"].where(
    df["Tons cut"] > 0,
    default_cut
)

# ----------------------
# Per-farm calculations
# ----------------------
df["Tons remaining"] = df["Tons"] - df["Tons cut"]

df["% cut"] = df.apply(
    lambda r: (r["Tons cut"] / r["Tons"] * 100) if r["Tons"] > 0 else 0,
    axis=1
)

# ----------------------
# Global calculations
# ----------------------
total_tons_to_remove = df["Tons cut"].sum()

required_bins = (
    total_tons_to_remove / bin_weight
    if bin_weight > 0 else 0
)

days_required = (
    required_bins / bins_per_day
    if bins_per_day > 0 else 0
)

# ----------------------
# Display results
# ----------------------
st.subheader("Per-farm results")
st.dataframe(df, use_container_width=True)

st.markdown("---")
st.subheader("Planning summary")

c1, c2, c3 = st.columns(3)

c1.metric("Total tons to remove", f"{total_tons_to_remove:.2f}")
c2.metric("Required bins", f"{required_bins:.2f}")
c3.metric("Days required", f"{days_required:.2f}")

# ----------------------
# Download
# ----------------------
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download per-farm results as CSV",
    csv,
    "tonnage_planning_results.csv",
    "text/csv"
)

st.session_state.data = edited_df
