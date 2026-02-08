import streamlit as st

st.set_page_config(page_title="BUTTON TEST", layout="centered")
st.title("BUTTON → NUMBER TEST")

# Widget key
CUT_KEY = "tons_cut"

# Initialise state
if CUT_KEY not in st.session_state:
    st.session_state[CUT_KEY] = 0.0

total_tons = st.number_input(
    "Total tons",
    value=1000.0,
    step=1.0
)

target_percent = st.number_input(
    "Target %",
    value=20.0,
    step=0.1
)

if st.button("APPLY %"):
    st.session_state[CUT_KEY] = total_tons * target_percent / 100

st.number_input(
    "Tons cut",
    key=CUT_KEY,
    step=1.0
)

st.write("Session state value:", st.session_state[CUT_KEY])
