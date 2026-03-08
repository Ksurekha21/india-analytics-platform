import streamlit as st
import pandas as pd
from utils.filters import get_filters
from utils.charts import create_chart
from utils.export_utils import chart_download_button, export_chart_to_pdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from PIL import Image


st.set_page_config(
    page_title="Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# LOAD CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------- FIX SESSION STATE --------

if "sector" not in st.session_state:

    st.warning("Please select a sector first.")

    if st.button("Go to Sectors Page"):
        st.switch_page("pages/1_Sectors.py")

    st.stop()

sector = st.session_state["sector"]

# -------- LOAD DATA --------

df = pd.read_csv(f"data/{sector}.csv")

state,district,start_year,end_year,metric,chart_type,analyze = get_filters(df)

filtered = df[
(df.state==state)&
(df.district==district)&
(df.year>=start_year)&
(df.year<=end_year)
]

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from PIL import Image

def generate_pdf(fig, sector, state, district, start_year, end_year, metric, avg, mx, mn, trend):

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    width, height = letter

    # -------- TITLE --------
    c.setFont("Helvetica-Bold", 18)
    c.drawString(180, height-40, "India Analytics Dashboard")

    # -------- FILTER DETAILS --------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height-80, "Report Details")

    c.setFont("Helvetica", 11)

    c.drawString(50, height-110, f"Sector: {sector}")
    c.drawString(50, height-130, f"State: {state}")
    c.drawString(50, height-150, f"District: {district}")
    c.drawString(50, height-170, f"Years: {start_year} - {end_year}")
    c.drawString(50, height-190, f"Metric: {metric}")

    # -------- KPI VALUES --------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height-230, "Key Metrics")

    c.setFont("Helvetica", 11)

    c.drawString(50, height-260, f"Average: {avg}")
    c.drawString(50, height-280, f"Maximum: {mx}")
    c.drawString(50, height-300, f"Minimum: {mn}")
    c.drawString(50, height-320, f"Trend: {trend}")

    # -------- CHART IMAGE --------
    img_bytes = fig.to_image(format="png")

    img_buffer = BytesIO(img_bytes)

    img = Image.open(img_buffer)

    img_path = "temp_chart.png"
    img.save(img_path)

    c.drawImage(img_path, 50, height-650, width=500, height=300)

    c.save()

    buffer.seek(0)

    return buffer

# ---------------- DASHBOARD ----------------

if analyze:

    # ---------- KPI CARDS ----------

    st.markdown("### Key Metrics")

    col1,col2,col3 = st.columns(3)

    col1.markdown(f"""
    <div class="kpi-card">
    <div class="kpi-title">Average</div>
    <div class="kpi-value">{round(filtered[metric].mean(),2)}</div>
    </div>
    """,unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="kpi-card">
    <div class="kpi-title">Maximum</div>
    <div class="kpi-value">{round(filtered[metric].max(),2)}</div>
    </div>
    """,unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="kpi-card">
    <div class="kpi-title">Minimum</div>
    <div class="kpi-value">{round(filtered[metric].min(),2)}</div>
    </div>
    """,unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- CHART ----------

    fig = create_chart(filtered,metric,chart_type)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    st.plotly_chart(fig,use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- DOWNLOAD BUTTON ----------

    col1,col2,col3 = st.columns([3,1,3])

    with col2:
        chart_download_button(fig)

        st.markdown("<br>", unsafe_allow_html=True)

    # ---------- INSIGHTS ----------

    st.markdown('<div class="insight-card">', unsafe_allow_html=True)

    st.subheader("Insights")

    avg = round(filtered[metric].mean(),2)
    mx = round(filtered[metric].max(),2)
    mn = round(filtered[metric].min(),2)

    st.write(f"Average {metric}: {avg}")
    st.write(f"Maximum {metric}: {mx}")
    st.write(f"Minimum {metric}: {mn}")

    trend = "Increasing 📈" if filtered[metric].iloc[-1] > filtered[metric].iloc[0] else "Decreasing 📉"

    st.write(f"Trend: {trend}")

    st.metric(
        "Current Value",
        round(filtered[metric].iloc[-1],2),
        round(filtered[metric].iloc[-1] - filtered[metric].iloc[-2],2)
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- DOWNLOAD PDF ----------
    avg = round(filtered[metric].mean(),2)
    mx = round(filtered[metric].max(),2)
    mn = round(filtered[metric].min(),2)

    trend = "Increasing 📈" if filtered[metric].iloc[-1] > filtered[metric].iloc[0] else "Decreasing 📉"

    pdf = generate_pdf(
        fig,
        sector,
        state,
        district,
        start_year,
        end_year,
        metric,
        avg,
        mx,
        mn,
        trend
    )


    export_chart_to_pdf(fig, "Dashboard Chart Report")