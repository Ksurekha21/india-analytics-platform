import streamlit as st
import pandas as pd
import plotly.express as px
import io
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from utils.filters import get_filters


st.set_page_config(page_title="District Analytics", layout="wide")

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

@st.cache_data
def load_data(sector):
    return pd.read_csv(f"data/{sector}.csv")

df = load_data(sector)

# -----------------------------
# FILTERS
# -----------------------------
state,district,start_year,end_year,metric,chart_type,analyze = get_filters(df)
# -----------------------------
# FILTER DATA
# -----------------------------
district_df = df[df["district"] == district]

state = district_df["state"].iloc[0]

filtered = district_df[
(district_df["year"] >= start_year) &
(district_df["year"] <= end_year)
]

state_filtered = df[
(df["state"] == state) &
(df["year"] >= start_year) &
(df["year"] <= end_year)
]

st.title(f"{district} District Analytics")

if analyze:

     # -----------------------------
    # KPI
    # -----------------------------
    col1,col2,col3 = st.columns(3)

    col1.metric("Average", round(filtered[metric].mean(),2))
    col2.metric("Maximum", round(filtered[metric].max(),2))
    col3.metric("Minimum", round(filtered[metric].min(),2))

   
    # =============================
    # DISTRICT TREND
    # =============================
    st.header("District Trend")

    yearly = (
        filtered
        .groupby("year")[metric]
        .mean()
        .reset_index()
    )

    if chart_type == "Line Chart":
        fig_trend = px.line(yearly,x="year",y=metric,markers=True)

    elif chart_type == "Bar Chart":
        fig_trend = px.bar(yearly,x="year",y=metric)

    elif chart_type == "Area Chart":
        fig_trend = px.area(yearly,x="year",y=metric)

    else:
        fig_trend = px.scatter(yearly,x="year",y=metric)

    st.plotly_chart(fig_trend,use_container_width=True)

    # =============================
    # DISTRICT VS STATE
    # =============================
    st.header("District vs State Comparison")

    district_year = (
        filtered.groupby("year")[metric]
        .mean()
        .reset_index()
    )

    state_year = (
        state_filtered.groupby("year")[metric]
        .mean()
        .reset_index()
    )

    district_year["type"] = "District"
    state_year["type"] = "State"

    comparison_df = pd.concat([district_year,state_year])

    fig_compare = px.line(
        comparison_df,
        x="year",
        y=metric,
        color="type",
        markers=True
    )

    st.plotly_chart(fig_compare,use_container_width=True)

    # =============================
    # GROWTH %
    # =============================
    st.header("District Growth %")

    yearly["growth"] = yearly[metric].pct_change() * 100

    fig_growth = px.line(
        yearly,
        x="year",
        y="growth",
        markers=True
    )

    st.plotly_chart(fig_growth,use_container_width=True)

     # =============================
    # DISTRICT RANK IN STATE
    # =============================
    ranking = (
        state_filtered
        .groupby("district")[metric]
        .mean()
        .sort_values(ascending=False)
    )

    rank = ranking.index.get_loc(district) + 1

    st.metric("District Rank in State", f"#{rank}")

    # =============================
    # DISTRICT CONTRIBUTION
    # =============================
    district_avg = filtered[metric].mean()

    state_avg = state_filtered[metric].mean()

    contribution = (district_avg / state_avg) * 100

    st.metric(
        "Contribution to State (%)",
        f"{round(contribution,2)}%"
    )
    # =============================
    # INSIGHTS
    # =============================
    st.header("Insights")

    best_year = yearly.loc[yearly[metric].idxmax()]["year"]
    worst_year = yearly.loc[yearly[metric].idxmin()]["year"]

    trend = "increasing 📈" if yearly[metric].iloc[-1] > yearly[metric].iloc[0] else "decreasing 📉"

    state_mean = state_filtered[metric].mean()

    if district_avg > state_mean:
        performance = "above the state average"
    else:
        performance = "below the state average"

    insights = [
    f"{district} ranks #{rank} in {state} based on average {metric}.",
    f"The district contributes approximately {round(contribution,2)}% to the overall state value.",
    f"The highest value occurred in {int(best_year)}.",
    f"The lowest value occurred in {int(worst_year)}.",
    f"The overall trend for {district} is {trend}.",
    f"{district} performs {performance}."
    ]

    for i in insights:
        st.write("•", i)

    # =============================
    # DOWNLOAD PDF
    # =============================
    st.header("Download District Analytics")

    charts = [
        ("District Trend",fig_trend),
        ("District vs State Comparison",fig_compare),
        ("District Growth",fig_growth)
    ]

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)

    y = 780

    c.setFont("Helvetica-Bold",18)
    c.drawString(150,y,f"{district} District Analytics")

    y -= 40

    c.setFont("Helvetica",12)
    c.drawString(50,y,f"Sector : {sector}")
    y -= 20
    c.drawString(50,y,f"State : {state}")
    y -= 20
    c.drawString(50,y,f"Metric : {metric}")

    y -= 40

    for title,fig in charts:

        c.setFont("Helvetica-Bold",14)
        c.drawString(50,y,title)

        img = fig.to_image(format="png")
        img_buffer = io.BytesIO(img)

        c.drawImage(ImageReader(img_buffer),50,y-250,width=500,height=250)

        y -= 300

        if y < 100:
            c.showPage()
            y = 780

    # =============================
    # INSIGHTS IN PDF
    # =============================
    c.showPage()

    c.setFont("Helvetica-Bold",16)
    c.drawString(200,780,"Insights")

    y = 740

    c.setFont("Helvetica",11)

    for insight in insights:

        c.drawString(60,y,insight)

        y -= 20

        if y < 100:
            c.showPage()
            y = 780

    c.save()

    pdf_buffer.seek(0)

    st.download_button(
    "Download District Analytics as PDF",
    pdf_buffer,
    f"{sector}_{district}_analytics.pdf",
    mime="application/pdf",
    key="download_pdf"
)