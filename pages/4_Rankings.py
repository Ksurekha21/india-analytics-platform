import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st
from utils.filters import get_filters
import io
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader




st.set_page_config(page_title="Rankings & Growth", layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# -------- Sector Check --------
sector = st.session_state.get("sector")

if sector is None:
    st.warning("Please select a sector first.")
    if st.button("Go to Sectors Page"):
        st.switch_page("pages/1_Sectors.py")
    st.stop()

# -------- Load Data --------
@st.cache_data
def load_data(sector):
    return pd.read_csv(f"data/{sector}.csv")

df = load_data(sector)

# -------- Filters --------
state,district,start_year,end_year,metric,chart_type,analyze = get_filters(
    df,
    show_state=False,
    show_district=False,
    show_chart_type=False
)

# -------- Filtered Data --------
filtered = df[
(df["year"] >= start_year) &
(df["year"] <= end_year)
]

st.title("Rankings & Growth Analysis")

# -------- Top/Bottom N --------
n = st.selectbox("Select Top / Bottom N", list(range(1,21)))

# ==============================
# STATE RANKINGS
# ==============================

st.header("Top States")

state_avg = (
    filtered
    .groupby("state")[metric]
    .mean()
    .reset_index()
)

top_states = state_avg.nlargest(n, metric)

fig = px.bar(
    top_states,
    y="state",
    x=metric,
    orientation="h",
    title="Top Performing States"
)

st.plotly_chart(fig, use_container_width=True)


st.header("Bottom States")

bottom_states = state_avg.nsmallest(n, metric)

fig = px.bar(
    bottom_states,
    y="state",
    x=metric,
    orientation="h",
    title="Lowest Performing States"
)

st.plotly_chart(fig, use_container_width=True)

# ==============================
# DISTRICT RANKINGS
# ==============================

st.header("Top Districts")

district_avg = (
    filtered
    .groupby("district")[metric]
    .mean()
    .reset_index()
)

top_districts = district_avg.nlargest(n, metric)

fig = px.bar(
    top_districts,
    y="district",
    x=metric,
    orientation="h",
    title="Top Performing Districts"
)

st.plotly_chart(fig, use_container_width=True)


st.header("Bottom Districts")

bottom_districts = district_avg.nsmallest(n, metric)

fig = px.bar(
    bottom_districts,
    y="district",
    x=metric,
    orientation="h",
    title="Lowest Performing Districts"
)

st.plotly_chart(fig, use_container_width=True)

# ==============================
# GROWTH ANALYSIS
# ==============================

st.header("Growth Analysis")

yearly = (
    filtered
    .groupby("year")[metric]
    .mean()
    .reset_index()
)

# Growth %
yearly["growth"] = yearly[metric].pct_change() * 100

# Highest / Lowest Growth
max_growth = yearly.loc[yearly["growth"].idxmax()]
min_growth = yearly.loc[yearly["growth"].idxmin()]

col1,col2 = st.columns(2)

col1.metric(
    "Year with Highest Growth",
    int(max_growth["year"]),
    f"{round(max_growth['growth'],2)}%"
)

col2.metric(
    "Year with Lowest Growth",
    int(min_growth["year"]),
    f"{round(min_growth['growth'],2)}%"
)

# Growth Line Chart
fig = px.line(
    yearly,
    x="year",
    y="growth",
    markers=True,
    title="Growth Trend Between Selected Years"
)

st.plotly_chart(fig, use_container_width=True)


from reportlab.lib.utils import ImageReader

pdf_buffer = io.BytesIO()

c = canvas.Canvas(pdf_buffer)

y = 780

# ---------- MAIN TITLE ----------
c.setFont("Helvetica-Bold",18)
c.drawString(120,y,"Rankings & Growth Analysis Report")

y -= 40

# ---------- SECTOR + METRIC ----------
c.setFont("Helvetica",12)
c.drawString(50,y,f"Sector : {sector.title()}")
y -= 20
c.drawString(50,y,f"Metric : {metric}")
y -= 30


# ---------- TOP STATES ----------
c.setFont("Helvetica-Bold",14)
c.drawString(50,y,"Top States")

fig = px.bar(top_states,y="state",x=metric,orientation="h")

img = fig.to_image(format="png")
img_buffer = io.BytesIO(img)

c.drawImage(
    ImageReader(img_buffer),
    50,
    y-260,
    width=500,
    height=250
)

y -= 280


# ---------- BOTTOM STATES ----------
c.setFont("Helvetica-Bold",14)
c.drawString(50,y,"Bottom States")

fig = px.bar(bottom_states,y="state",x=metric,orientation="h")

img = fig.to_image(format="png")
img_buffer = io.BytesIO(img)

c.drawImage(
    ImageReader(img_buffer),
    50,
    y-260,
    width=500,
    height=250
)

y -= 280


# ---------- NEW PAGE ----------
c.showPage()

y = 780


# ---------- TOP DISTRICTS ----------
c.setFont("Helvetica-Bold",14)
c.drawString(50,y,"Top Districts")

fig = px.bar(top_districts,y="district",x=metric,orientation="h")

img = fig.to_image(format="png")
img_buffer = io.BytesIO(img)

c.drawImage(
    ImageReader(img_buffer),
    50,
    y-260,
    width=500,
    height=250
)

y -= 280


# ---------- BOTTOM DISTRICTS ----------
c.setFont("Helvetica-Bold",14)
c.drawString(50,y,"Bottom Districts")

fig = px.bar(bottom_districts,y="district",x=metric,orientation="h")

img = fig.to_image(format="png")
img_buffer = io.BytesIO(img)

c.drawImage(
    ImageReader(img_buffer),
    50,
    y-260,
    width=500,
    height=250
)

y -= 280


# ---------- NEW PAGE ----------
c.showPage()

y = 780


# ---------- GROWTH ANALYSIS ----------
c.setFont("Helvetica-Bold",16)
c.drawString(200,y,"Growth Analysis")

y -= 40

c.setFont("Helvetica",12)

c.drawString(50,y,f"Year with Highest Growth : {int(max_growth['year'])} ({round(max_growth['growth'],2)}%)")
y -= 20

c.drawString(50,y,f"Year with Lowest Growth : {int(min_growth['year'])} ({round(min_growth['growth'],2)}%)")

y -= 40


# ---------- GROWTH CHART ----------
fig = px.line(yearly,x="year",y="growth")

img = fig.to_image(format="png")
img_buffer = io.BytesIO(img)

c.drawImage(
    ImageReader(img_buffer),
    50,
    y-300,
    width=500,
    height=300
)

c.save()

pdf_buffer.seek(0)


st.download_button(
    "Download Rankings & Growth Analysis as PDF",
    pdf_buffer,
    f"{sector}_rankings_and_growth.pdf",
    mime="application/pdf",
    key="download_pdf"
)