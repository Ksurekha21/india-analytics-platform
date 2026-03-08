import streamlit as st

import streamlit as st

st.set_page_config(
    page_title="India Analytics Platform",
    layout="wide"
)

# hide default sidebar navigation
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)
# LOAD CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.sidebar.title("🇮🇳 India Analytics")

st.sidebar.page_link("app.py", label="🏠 Home")
st.sidebar.page_link("pages/1_Sectors.py", label="📊 Sectors")
st.sidebar.page_link("pages/2_Dashboard.py", label="📈 Dashboard")
st.sidebar.page_link("pages/3_All_Charts.py", label="📉 All Charts")
st.sidebar.page_link("pages/4_Rankings.py", label="🏆 Rankings")
st.sidebar.page_link("pages/5_Comparison.py", label="⚖ Comparison")
st.sidebar.page_link("pages/6_State_Analytics.py", label="📍 State Analytics")
st.sidebar.page_link("pages/7_District_Analytics.py", label="📍 District Analytics")
st.sidebar.page_link("pages/8_Forecasting.py", label="🔮 Forecasting")
st.sidebar.page_link("pages/9_National_Summary.py", label="📊 National Summary")
st.sidebar.page_link("pages/10_AI_Chatbot.py", label="🤖 AI Chatbot")


st.sidebar.markdown("---")


# ---------- HERO SECTION ----------

col1, col2 = st.columns([3,2])

with col1:
    st.title("🇮🇳 India Analytics Platform")
    st.write("Explore India's Data with AI Powered Analytics")

    st.write("")

    if st.button("🚀 Enter Platform"):
        st.switch_page("pages/1_Sectors.py")

