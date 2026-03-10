import streamlit as st
import pandas as pd
import plotly.express as px
import io
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


st.set_page_config(page_title="National Summary", layout="wide")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -----------------------------
# SECTOR CHECK
# -----------------------------

sector = st.session_state.get("sector")

if sector is None:
    st.warning("Please select a sector first.")
    if st.button("Go to Sectors Page"):
        st.switch_page("pages/1_Sectors.py")
    st.stop()

# -----------------------------
# LOAD DATA
# -----------------------------

@st.cache_data
def load_data(sector):
    return pd.read_csv(f"data/{sector}.csv")

df = load_data(sector)

st.title("National Summary Dashboard")

# -----------------------------
# METRIC SELECTOR
# -----------------------------

metric = st.sidebar.selectbox(
    "Select Metric",
    [c for c in df.columns if c not in ["state","district","year"]]
)

# -----------------------------
# STATE AVERAGES
# -----------------------------

state_avg = df.groupby("state")[metric].mean().reset_index()

best_state = state_avg.loc[state_avg[metric].idxmax()]
worst_state = state_avg.loc[state_avg[metric].idxmin()]

# -----------------------------
# NATIONAL GROWTH
# -----------------------------

yearly = df.groupby("year")[metric].mean().reset_index()

yearly["growth"] = yearly[metric].pct_change()*100

highest_growth = yearly.loc[yearly["growth"].idxmax()]
lowest_growth = yearly.loc[yearly["growth"].idxmin()]

# =============================
# FEATURE 1
# NATIONAL KPI CARDS
# =============================



col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Best State",
    best_state["state"],
    round(best_state[metric],2)
)

col2.metric(
    "Worst State",
    worst_state["state"],
    round(worst_state[metric],2)
)

col3.metric(
    "Highest Growth Year",
    int(highest_growth["year"]),
    f"{round(highest_growth['growth'],2)}%"
)

col4.metric(
    "Lowest Growth Year",
    int(lowest_growth["year"]),
    f"{round(lowest_growth['growth'],2)}%"
)

st.divider()


# =============================

# =============================
# FEATURE 4
# SECTOR TREND
# =============================

st.header("National Trend Over Years")

fig_trend = px.line(
    yearly,
    x="year",
    y=metric,
    markers=True,
    title="India Trend Over Years"
)

st.plotly_chart(fig_trend,use_container_width=True)



#
# =============================
# FEATURE 6
# STATE CONTRIBUTION CHART
# =============================

st.divider()

st.header("State Contribution Chart")

state_total = df.groupby("state")[metric].sum().reset_index()

fig_pie = px.pie(
    state_total,
    values=metric,
    names="state",
    title="State Contribution to National Total"
)

st.plotly_chart(fig_pie,use_container_width=True)

# =============================
# FEATURE
# TOP STATE IN INDIA
# =============================

st.divider()

st.header("Top State in India")

state_avg = df.groupby("state")[metric].mean().reset_index()

top_state = state_avg.loc[state_avg[metric].idxmax()]

st.metric(
    "Top State in India",
    top_state["state"],
    round(top_state[metric],2)
)

# =============================
# FEATURE 7
# TOP DISTRICT IN INDIA
# =============================

st.divider()

st.header("Top District in India")

district_avg = df.groupby(["state","district"])[metric].mean().reset_index()

best_district = district_avg.loc[district_avg[metric].idxmax()]

st.metric(
    "Best Performing District",
    best_district["district"],
    f"{best_district['state']} | {round(best_district[metric],2)}"
)


# FEATURE 5
# NATIONAL GROWTH INDICATOR
# =============================
st.divider()

st.header("National Growth Indicator")

overall_growth = (
    (yearly[metric].iloc[-1] - yearly[metric].iloc[0]) /
    yearly[metric].iloc[0]
) * 100

st.metric(
    "Overall Growth %",
    f"{round(overall_growth,2)}%"
)

import io
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader



charts = [
    
    ("India Trend Over Years", fig_trend),
    ("State Contribution Chart", fig_pie)
]

pdf_buffer = io.BytesIO()
c = canvas.Canvas(pdf_buffer)

y = 780

# -----------------------------
# REPORT TITLE
# -----------------------------
c.setFont("Helvetica-Bold",18)
c.drawString(140,y,"National Summary Dashboard Report")

y -= 40

c.setFont("Helvetica",12)
c.drawString(50,y,f"Sector : {sector}")
y -= 20
c.drawString(50,y,f"Metric : {metric}")

y -= 40


# -----------------------------
# KPI SECTION
# -----------------------------
c.setFont("Helvetica-Bold",14)
c.drawString(50,y,"National KPI Summary")

y -= 20

c.setFont("Helvetica",11)

c.drawString(60,y,f"Best State : {best_state['state']} ({round(best_state[metric],2)})")
y -= 20
c.drawString(60,y,f"Worst State : {worst_state['state']} ({round(worst_state[metric],2)})")
y -= 20
c.drawString(60,y,f"Highest Growth Year : {int(highest_growth['year'])} ({round(highest_growth['growth'],2)}%)")
y -= 20
c.drawString(60,y,f"Lowest Growth Year : {int(lowest_growth['year'])} ({round(lowest_growth['growth'],2)}%)")

y -= 40


# -----------------------------
# CHARTS
# -----------------------------
for title,fig in charts:

    c.setFont("Helvetica-Bold",14)
    c.drawString(50,y,title)

    img = fig.to_image(format="png")
    img_buffer = io.BytesIO(img)

    c.drawImage(
        ImageReader(img_buffer),
        50,
        y-250,
        width=500,
        height=250
    )

    y -= 300

    if y < 120:
        c.showPage()
        y = 780

import io
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

st.divider()

st.header("Download National Summary Report")

charts = [
    
    ("India Trend Over Years", fig_trend),
    ("State Contribution Chart", fig_pie)
]

pdf_buffer = io.BytesIO()
c = canvas.Canvas(pdf_buffer)

y = 780

# -----------------------------
# REPORT TITLE
# -----------------------------
c.setFont("Helvetica-Bold",18)
c.drawString(140,y,"National Summary Dashboard Report")

y -= 40

c.setFont("Helvetica",12)
c.drawString(50,y,f"Sector : {sector}")
y -= 20
c.drawString(50,y,f"Metric : {metric}")

y -= 40


# -----------------------------
# KPI SECTION
# -----------------------------
c.setFont("Helvetica-Bold",14)
c.drawString(50,y,"National KPI Summary")

y -= 20

c.setFont("Helvetica",11)

c.drawString(60,y,f"Best State : {best_state['state']} ({round(best_state[metric],2)})")
y -= 20
c.drawString(60,y,f"Worst State : {worst_state['state']} ({round(worst_state[metric],2)})")
y -= 20
c.drawString(60,y,f"Highest Growth Year : {int(highest_growth['year'])} ({round(highest_growth['growth'],2)}%)")
y -= 20
c.drawString(60,y,f"Lowest Growth Year : {int(lowest_growth['year'])} ({round(lowest_growth['growth'],2)}%)")

y -= 40


# -----------------------------
# CHARTS
# -----------------------------
for title,fig in charts:

    c.setFont("Helvetica-Bold",14)
    c.drawString(50,y,title)

    img = fig.to_image(format="png")
    img_buffer = io.BytesIO(img)

    c.drawImage(
        ImageReader(img_buffer),
        50,
        y-250,
        width=500,
        height=250
    )

    y -= 300

    if y < 120:
        c.showPage()
        y = 780


# -----------------------------
# TOP STATE IN INDIA
# -----------------------------

y -= 20

c.setFont("Helvetica-Bold",14)
c.drawString(50,y,"Top State in India")

y -= 20

c.setFont("Helvetica",11)

c.drawString(
    60,
    y,
    f"{top_state['state']} : {round(top_state[metric],2)}"
)

y -= 30
# -----------------------------
# TOP DISTRICT
# -----------------------------
c.showPage()

c.setFont("Helvetica-Bold",16)
c.drawString(200,780,"Top District in India")

y = 740

c.setFont("Helvetica",12)

c.drawString(
    60,
    y,
    f"{best_district['district']} ({best_district['state']}) : {round(best_district[metric],2)}"
)

c.save()

pdf_buffer.seek(0)

st.download_button(
    "Download National Summary as PDF",
    pdf_buffer,
    f"{sector}_national_summary.pdf",
    mime="application/pdf",
    key="download_pdf"
)