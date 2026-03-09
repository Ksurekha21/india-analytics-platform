import streamlit as st
import pandas as pd
import io
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from utils.charts import create_chart
from utils.filters import get_filters
from io import BytesIO

st.set_page_config(
    page_title="All Charts",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- CHECK SECTOR ----------
sector = st.session_state.get("sector")

if sector is None:
    st.warning("Please select a sector first.")
    st.stop()

# ---------- LOAD DATA ----------
df = pd.read_csv(f"data/{sector}.csv")

state, district, start_year, end_year, metric, chart_type, analyze = get_filters(df, show_chart_type=False)

filtered = df[
    (df.state == state) &
    (df.district == district) &
    (df.year >= start_year) &
    (df.year <= end_year)
]

st.title("All Charts")

# ---------- SHOW CHARTS ONLY AFTER ANALYZE ----------
if analyze:

    chart_list = [
        "Line Chart","Multi-Line Chart","Area Chart","Step Line","Spline",
        "Bar Chart","Horizontal Bar","Grouped Bar","Stacked Bar","100% Stacked",
        "Histogram","Box Plot","Density Plot","Violin Plot",
        "Pareto Chart","Control Chart","Waterfall Chart","Funnel Chart"
    ]

    chart_images = []

    for i in range(0, len(chart_list), 2):

        col1, col2 = st.columns(2)

        # ---------- CHART 1 ----------
        chart1 = chart_list[i]
        fig1 = create_chart(filtered, metric, chart1)

        col1.subheader(chart1)
        col1.plotly_chart(fig1, use_container_width=True)

        img1 = fig1.to_image(format="png")
        chart_images.append(img1)

        col1.download_button(
            "⬇ Download Chart",
            img1,
            file_name=f"{metric}_{chart1}.png",
            mime="image/png",
            key=f"download_{chart1}_{i}"
        )

        # ---------- CHART 2 ----------
        if i + 1 < len(chart_list):

            chart2 = chart_list[i + 1]
            fig2 = create_chart(filtered, metric, chart2)

            col2.subheader(chart2)
            col2.plotly_chart(fig2, use_container_width=True)

            img2 = fig2.to_image(format="png")
            chart_images.append(img2)

            col2.download_button(
                "⬇ Download Chart",
                img2,
                file_name=f"{metric}_{chart2}.png",
                mime="image/png",
                key=f"download_{chart2}_{i}"
            )

    # ---------- PDF EXPORT ----------
    st.header("Download All Charts")

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)

    y = 780

    # ---------- TITLE ----------
    c.setFont("Helvetica-Bold", 18)
    c.drawString(160, y, "All Charts Report")

    y -= 40

    # ---------- FILTER DETAILS ----------
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Sector : {sector.title()}"); y -= 20
    c.drawString(50, y, f"State : {state}"); y -= 20
    c.drawString(50, y, f"District : {district}"); y -= 20
    c.drawString(50, y, f"Metric : {metric}")

    y -= 40

    # ---------- CHART LOOP ----------
    for chart_name, img in zip(chart_list, chart_images):

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, chart_name)

        y -= 10

        image = ImageReader(BytesIO(img))

        c.drawImage(
            image,
            50,
            y - 300,
            width=500,
            height=300
        )

        y -= 320

        if y < 100:
            c.showPage()
            y = 780

    c.save()
    pdf_buffer.seek(0)

    st.download_button(
        "Download All Charts as PDF",
        pdf_buffer,
        f"{sector}_all_charts.pdf",
        mime="application/pdf",
        key="download_pdf_all_charts"
    )