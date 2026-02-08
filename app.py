import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tonnage Cut Calculator", layout="wide")

st.title("Tonnage Reduction Calculator")

cut_percentage = st.number_input(
    "Global Percentage Cut (%)",
    min_value=0.0,
    max_value=100.0,
    value=20.0,
    step=0.5
)

st.markdown("---")

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Farm No": ["Farm 1"],
        "Tonnes": [0.0]
    })

edited_df = st.data_editor(
    st.session_state.data,
    num_rows="dynamic",
    use_container_width=True
)

df = edited_df.copy()

df["Tonnes Cut"] = df["Tonnes"] * (cut_percentage / 100)
df["Tonnes Remaining"] = df["Tonnes"] - df["Tonnes Cut"]

df["% Cut"] = df.apply(
    lambda row: (row["Tonnes Cut"] / row["Tonnes"] * 100)
    if row["Tonnes"] > 0 else 0,
    axis=1
)

st.markdown("---")
st.subheader("Results")

st.dataframe(df, use_container_width=True)

st.session_state.data = edited_df

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Results as CSV",
    csv,
    "tonnage_cut_results.csv",
    "text/csv"
)
