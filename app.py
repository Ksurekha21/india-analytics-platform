import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="India Analytics Platform", page_icon="📈", layout="wide")

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem; margin-top: 1rem;">
    <h1 style="
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        color: transparent;
        margin-bottom: 0.5rem;
    ">
        India Data Analytics Platform
    </h1>
    <p style="font-size: 1.25rem; color: var(--text-color); opacity: 0.8; font-weight: 500;">
        Unlock the Power of Data Across India's States & Districts
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- CSS & NAVIGATION OVERRIDES ----------
custom_home_css = """
<style>
/* Hide the default sidebar navigation since we manually build it */
[data-testid="stSidebarNav"] {display:none;}

/* Global Font Override */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Feature Card Styling */
.feature-card {
    background: var(--secondary-background-color);
    padding: 28px 24px;
    border-radius: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    border: 1px solid rgba(128, 128, 128, 0.15);
    height: 100%;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    text-align: center;
    position: relative;
    overflow: hidden;
}
.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 16px 32px rgba(37, 99, 235, 0.15);
    border-color: rgba(37, 99, 235, 0.4);
}
.feature-icon {
    font-size: 42px;
    margin-bottom: 16px;
}
.feature-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 12px;
}
.feature-desc {
    font-size: 0.95rem;
    color: var(--text-color);
    opacity: 0.85;
    line-height: 1.6;
}

/* Floating animation for Logo */
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-12px); }
    100% { transform: translateY(0px); }
}

/* Style main CTA Button on this page */
div[data-testid="stMainBlockContainer"] .stButton button[kind="secondary"] {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white !important;
    border: none;
    border-radius: 14px;
    padding: 10px 32px;
    font-weight: 700;
    transition: all 0.3s ease;
    box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);
}

div[data-testid="stMainBlockContainer"] .stButton button[kind="secondary"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 25px rgba(37, 99, 235, 0.35);
    background: linear-gradient(135deg, #1d4ed8, #6d28d9);
}

div[data-testid="stMainBlockContainer"] .stButton button[kind="secondary"] p {
    font-size: 1.15rem;
    color: white;
}
</style>
"""
st.markdown(custom_home_css, unsafe_allow_html=True)

# ---------- LOAD CSS ----------
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

# ---------- SIDEBAR ----------
st.sidebar.title("India Analytics")

st.sidebar.page_link("app.py", label="🏠 Home")
st.sidebar.page_link("pages/1_Sectors.py", label="📊 Sectors")
st.sidebar.page_link("pages/2_Dashboard.py", label="📈 Dashboard")
st.sidebar.page_link("pages/3_All_Charts.py", label="📉 All Charts")
st.sidebar.page_link("pages/4_Rankings.py", label="🏆 Rankings")
st.sidebar.page_link("pages/5_Comparison.py", label="⚖️ Comparison")
st.sidebar.page_link("pages/6_State_Analytics.py", label="📍 State Analytics")
st.sidebar.page_link("pages/7_District_Analytics.py", label="📍 District Analytics")
st.sidebar.page_link("pages/8_Forecasting.py", label="🔮 Forecasting")
st.sidebar.page_link("pages/9_National_Summary.py", label="📊 National Summary")
st.sidebar.page_link("pages/10_AI_Chatbot.py", label="🤖 AI Chatbot")

st.sidebar.markdown("---")

# ---------- HERO SECTION ----------
col1, col2, col3 = st.columns([1.5, 2, 1.5])

with col2:
    st.markdown("<div style='text-align: center;'><img src='https://cdn-icons-png.flaticon.com/512/2103/2103658.png' width='220' style='margin-bottom: 30px; animation: float 6s ease-in-out infinite;'></div>", unsafe_allow_html=True)
    if st.button("🚀 Enter Platform", use_container_width=True):
        st.switch_page("pages/1_Sectors.py")

st.write("")
st.write("")
st.write("")
st.write("")

# ---------- FEATURES ----------

st.markdown("<h2 style='text-align: center; margin-bottom: 2.5rem; color: var(--text-color); font-weight: 800; font-size: 2rem;'>Platform Features</h2>", unsafe_allow_html=True)

def render_feature(icon, title, desc):
    return f"""
    <div class="feature-card">
        <div class="feature-icon">{icon}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-desc">{desc}</div>
    </div>
    """

# Top Row
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(render_feature("📊", "Interactive Charts", "Explore multiple visualizations including detailed line charts, bar charts, histograms and more."), unsafe_allow_html=True)

with col2:
    st.markdown(render_feature("🗺️", "State & District Insights", "Analyze demographic and economic trends across India's states and districts with dynamic filters."), unsafe_allow_html=True)

with col3:
    st.markdown(render_feature("📄", "Export Reports", "Download your charts and comprehensive analytics reports in PDF format for presentations."), unsafe_allow_html=True)

st.write("")
st.write("")

# Bottom Row - centered
_, c1, c2, _ = st.columns([1, 2, 2, 1])

with c1:
    st.markdown(render_feature("🔮", "Insights & Forecasting", "Predict future economic and developmental trends using machine learning models and historical data."), unsafe_allow_html=True)

with c2:
    st.markdown(render_feature("🤖", "AI Data Assistant", "Ask complex questions about your data and instantly get smart insights powered by state-of-the-art Generative AI."), unsafe_allow_html=True)

st.write("")
st.write("")

# ---------- FOOTER ----------
st.markdown("""
<hr style="border-top: 1px solid var(--text-color); opacity: 0.2; margin-top: 4rem; margin-bottom: 2rem;">
<div style="text-align: center; color: var(--text-color); opacity: 0.85; font-size: 0.95rem;">
    <b style="font-size: 1.05rem;">India Data Analytics Platform</b><br><br>
    Built with <b>Streamlit</b> • AI Powered Analytics
</div>
<br>
""", unsafe_allow_html=True)