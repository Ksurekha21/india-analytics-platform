import streamlit as st

st.markdown("""
<h1 style="
text-align:center;
font-size:3.1vw;
white-space:nowrap;
font-weight:800;
background: linear-gradient(90deg,#2563eb,#7c3aed);
-webkit-background-clip: text;
color: transparent;
">
India Data Analytics Platform
</h1>
""", unsafe_allow_html=True)

# ---------- HIDE DEFAULT NAV ----------
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display:none;}
</style>
""", unsafe_allow_html=True)

# ---------- LOAD CSS ----------
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("India Analytics")

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
    st.markdown(
        "<h1></h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h2 style='font-size:16px;'>
        Unlock the Power of Data Across India's States & Districts
        </h2>
        """,
        unsafe_allow_html=True
    )
    st.write("")

    if st.button("🚀 Enter Platform", use_container_width=True):
        st.switch_page("pages/1_Sectors.py")

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103658.png", width=280)

st.write("")
st.write("")

# ---------- FEATURES ----------


st.subheader("Platform Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📊 Interactive Charts
    Explore multiple visualizations including line charts, bar charts, histograms and more.
    """)

with col2:
    st.markdown("""
    ### 🗺 State & District Insights
    Analyze trends across India's states and districts with powerful filters.
    """)

with col3:
    st.markdown("""
    ### 📄 Export Reports
    Download charts and full reports in PDF for presentations and analysis.
    """)

st.write("")

col4, col5 = st.columns(2)

with col4:
    st.markdown("""
    ### 🔮 Insights
    Predict future trends using machine learning models and historical data.
    """)

with col5:
    st.markdown("""
    ### 🤖 AI Data Assistant
    Ask questions about data and get instant insights powered by AI.
    """)


# ---------- FOOTER ----------
st.markdown("""
---
<center>
<b>India Data Analytics Platform</b><br>
Built with Streamlit • AI Powered Analytics
</center>
""", unsafe_allow_html=True)