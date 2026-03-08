import streamlit as st
import streamlit as st

st.set_page_config(
    page_title="Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(
"""
<h1 style='text-align:center;color:#4B8BBE;font-size:48px;margin-top:100px;'>
Select Sector
</h1>
""",
unsafe_allow_html=True
)

sectors = {
"Pollution":"📊",
"Agriculture":"🌾",
"Energy":"⚡",
"Population":"👥",
"Literacy":"📚",
"Transport":"🚗",
"Tourism":"🧳",
"Education":"🎓",
"Hospital":"🏥",
"Climate":"🌍",
"Employment":"💼",
"Economy":"📉",
"Infrastructure":"🏗",
"Technology":"💻",
"Smart Cities":"🏙",
"Crime":"🚓",
"Health":"🩺",
"Water":"💧",
"housing":"🏠",
"Finance":"💰",
"industry":"🏭",
"rural development":"🌾",
"urban development":"🏙",
"internet":"🌐",
"sports":"🏅",
"poverty":"🪙",
"nutrition":"🍎",
"trade":"📦"

}

# create 4 equal columns
col1, col2, col3, col4 = st.columns(4)

cols = [col1, col2, col3, col4]

for i,(sector,icon) in enumerate(sectors.items()):

    with cols[i % 4]:

        if st.button(f"{icon} {sector}", use_container_width=True):

            st.session_state["sector"] = sector.lower().replace(" ","_")

            st.switch_page("pages/2_Dashboard.py")