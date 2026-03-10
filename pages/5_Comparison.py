import streamlit as st
import pandas as pd
import plotly.express as px
import io
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from utils.filters import get_filters


st.set_page_config(page_title="Comparison", layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------- Sector check --------
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
    show_year=True,
    show_chart_type=True
)

filtered = df[
(df.year>=start_year) &
(df.year<=end_year)
]

st.header("State vs State Comparison")

col1,col2 = st.columns(2)

state1 = col1.selectbox(
    "Select First State",
    sorted(filtered["state"].unique())
)

state2 = col2.selectbox(
    "Select Second State",
    sorted(filtered["state"].unique())
)

if analyze:

    state_df = filtered[
        filtered["state"].isin([state1,state2])
    ]

    state_df = (
        state_df
        .groupby(["year","state"])[metric]
        .mean()
        .reset_index()
    )

    if chart_type == "Bar Chart":
        fig_state = px.bar(
            state_df,
            x="year",
            y=metric,
            color="state",
            barmode="group"
        )
    else:
        fig_state = px.line(
            state_df,
            x="year",
            y=metric,
            color="state",
            markers=True
        )

    st.plotly_chart(fig_state,use_container_width=True)


    # Download chart
    st.download_button(
    "⬇ Download State Chart",
    fig_state.to_image(format="png"),
    f"{metric}_state_comparison.png",
    mime="image/png",
    key="download_state_chart"
)

    # -------- Comparison Table --------

    st.header("Comparison Table")

    table = pd.concat([
        state_df.rename(columns={"state":"region"}),
        
    ])

    st.dataframe(table,use_container_width=True)

# -------- District Comparison --------

st.header("District vs District Comparison")

col3,col4 = st.columns(2)

district1 = col3.selectbox(
    "Select First District",
    sorted(filtered["district"].unique())
)

district2 = col4.selectbox(
    "Select Second District",
    sorted(filtered["district"].unique())
)

if analyze:

    district_df = filtered[
        filtered["district"].isin([district1,district2])
    ]

    district_df = (
        district_df
        .groupby(["year","district"])[metric]
        .mean()
        .reset_index()
    )

    if chart_type == "Bar Chart":
        fig_district = px.bar(
            district_df,
            x="year",
            y=metric,
            color="district",
            barmode="group"
        )
    else:
        fig_district = px.line(
            district_df,
            x="year",
            y=metric,
            color="district",
            markers=True
        )

    st.plotly_chart(fig_district,use_container_width=True)

    st.download_button(
    "⬇ Download District Chart",
    fig_district.to_image(format="png"),
    f"{metric}_district_comparison.png",
    mime="image/png",
    key="download_district_chart"
)
# -------- Comparison Table --------

    st.header("Comparison Table")

    table = pd.concat([
        
        district_df.rename(columns={"district":"region"})
    ])

    st.dataframe(table,use_container_width=True)
# -------- PDF Export --------

    st.header("Download Comparison Report")

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)

    y = 780

    # ---------- TITLE ----------
    c.setFont("Helvetica-Bold",18)
    c.drawString(150,y,"Comparison Report")

    y -= 40

    c.setFont("Helvetica",12)
    c.drawString(50,y,f"Sector : {sector}")
    y -= 20
    c.drawString(50,y,f"Metric : {metric}")

    y -= 40


    # ---------- STATE GRAPH ----------
    c.setFont("Helvetica-Bold",14)
    c.drawString(50,y,"State vs State Comparison")

    img = fig_state.to_image(format="png")
    img_buffer = io.BytesIO(img)

    c.drawImage(ImageReader(img_buffer),50,y-250,width=500,height=250)

    y -= 280


    # ---------- STATE TABLE ----------
    c.setFont("Helvetica-Bold",14)
    c.drawString(50,y,"State Comparison Table")

    y -= 25

    c.setFont("Helvetica",10)

    for i,row in state_df.iterrows():

        line = f"{row['year']} | {row['state']} | {round(row[metric],2)}"
        c.drawString(60,y,line)

        y -= 15

        if y < 100:
            c.showPage()
            y = 780


    # ---------- DISTRICT GRAPH ----------
    y -= 30

    c.setFont("Helvetica-Bold",14)
    c.drawString(50,y,"District vs District Comparison")

    img = fig_district.to_image(format="png")
    img_buffer = io.BytesIO(img)

    c.drawImage(ImageReader(img_buffer),50,y-250,width=500,height=250)

    y -= 280


    # ---------- DISTRICT TABLE ----------
    c.setFont("Helvetica-Bold",14)
    c.drawString(50,y,"District Comparison Table")

    y -= 25

    c.setFont("Helvetica",10)

    for i,row in district_df.iterrows():

        line = f"{row['year']} | {row['district']} | {round(row[metric],2)}"
        c.drawString(60,y,line)

        y -= 15

        if y < 100:
            c.showPage()
            y = 780


    c.save()

    st.download_button(
    "⬇ Download Comparison Report as PDF",
    pdf_buffer,
    f"{sector}_comparison_report.pdf",
    mime="application/pdf",
    key="download_comparison_pdf"
)

    