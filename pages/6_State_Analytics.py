import streamlit as st
import pandas as pd
import plotly.express as px
import io
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from utils.filters import get_filters

st.set_page_config(page_title="State Analytics", layout="wide")
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

df = pd.read_csv(f"data/{sector}.csv")

# -----------------------------
# FILTERS
# -----------------------------
state,district,start_year,end_year,metric,chart_type,analyze = get_filters(
    df,
    show_district=False,
)
# -----------------------------
# FILTER DATA
# -----------------------------
filtered = df[
(df["state"]==state) &
(df["year"]>=start_year) &
(df["year"]<=end_year)
]

st.title(f"{state} State Analytics")

if analyze:

    # -----------------------------
    # KPI
    # -----------------------------
    col1,col2,col3 = st.columns(3)

    col1.metric("Average", round(filtered[metric].mean(),2))
    col2.metric("Maximum", round(filtered[metric].max(),2))
    col3.metric("Minimum", round(filtered[metric].min(),2))

    # -----------------------------
    # STATE TREND
    # -----------------------------
    st.header("State Trend")

    yearly = filtered.groupby("year")[metric].mean().reset_index()

    if chart_type=="Line Chart":
        fig_trend = px.line(yearly,x="year",y=metric,markers=True)

    elif chart_type=="Bar Chart":
        fig_trend = px.bar(yearly,x="year",y=metric)

    elif chart_type=="Area Chart":
        fig_trend = px.area(yearly,x="year",y=metric)

    elif chart_type=="Scatter Plot":
        fig_trend = px.scatter(yearly,x="year",y=metric)

    elif chart_type=="Box Plot":
        fig_trend = px.box(filtered,x="year",y=metric)

    elif chart_type=="Histogram":
        fig_trend = px.histogram(filtered,x=metric)

    else:
        fig_trend = px.violin(filtered,x="year",y=metric)

    st.plotly_chart(fig_trend,use_container_width=True)

    # -----------------------------
    # TOP DISTRICTS
    # -----------------------------
    st.header("Top Districts")

    district_avg = (
        filtered.groupby("district")[metric]
        .mean()
        .reset_index()
    )

    top_districts = district_avg.nlargest(10,metric)

    fig_top = px.bar(
        top_districts,
        x=metric,
        y="district",
        orientation="h"
    )

    st.plotly_chart(fig_top,use_container_width=True)

    # -----------------------------
    # BOTTOM DISTRICTS
    # -----------------------------
    st.header("Bottom Districts")

    bottom_districts = district_avg.nsmallest(10,metric)

    fig_bottom = px.bar(
        bottom_districts,
        x=metric,
        y="district",
        orientation="h"
    )

    st.plotly_chart(fig_bottom,use_container_width=True)

    # -----------------------------
    # DISTRICT CONTRIBUTION
    # -----------------------------
    # -----------------------------
# DISTRICT CONTRIBUTION (ALL DISTRICTS)
# -----------------------------
    st.header("District Contribution (All Districts)")

    district_avg = (
        filtered
        .groupby("district")[metric]
        .mean()
        .reset_index()
    )

    # Sort for better visualization
    district_avg = district_avg.sort_values(metric, ascending=False)

    fig_pie = px.pie(
        district_avg,
        names="district",
        values=metric,
        title=f"{state} District Contribution",
        hole=0.3
    )

    fig_pie.update_traces(textposition="inside", textinfo="percent+label")

    st.plotly_chart(fig_pie, use_container_width=True)

    # -----------------------------
    # HEATMAP
    # -----------------------------
    # -----------------------------
# DISTRICT HEATMAP (ALL DISTRICTS)
# -----------------------------
    st.header("District Heatmap (All Districts)")

    heatmap_df = (
        filtered
        .groupby(["district","year"])[metric]
        .mean()
        .reset_index()
    )

    pivot = heatmap_df.pivot(
        index="district",
        columns="year",
        values=metric
    )

    # Fill missing values so districts don't disappear
    pivot = pivot.fillna(0)

    fig_heat = px.imshow(
        pivot,
        labels=dict(
            x="Year",
            y="District",
            color=metric
        ),
        title=f"{state} District Heatmap"
    )

    fig_heat.update_layout(
        height=800   # important when many districts exist
    )

    st.plotly_chart(fig_heat, use_container_width=True)

    # -----------------------------
    # INSIGHTS
    # -----------------------------
    st.header("Insights")

    best = district_avg.nlargest(1,metric).iloc[0]["district"]

    st.write(f"Best district in {state}: {best}")
    st.write(f"Average {metric}: {round(filtered[metric].mean(),2)}")

    # -----------------------------
    # DOWNLOAD PDF
    # -----------------------------
    st.header("Download State Analytics")

    charts = [
        ("State Trend",fig_trend),
        ("Top Districts",fig_top),
        ("Bottom Districts",fig_bottom),
        ("District Contribution",fig_pie),
        ("District Heatmap",fig_heat)
    ]

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)

    y = 780

    c.setFont("Helvetica-Bold",18)
    c.drawString(150,y,f"{state} State Analytics")

    y -= 40

    c.setFont("Helvetica",12)
    c.drawString(50,y,f"Sector : {sector}")
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

    c.save()

    pdf_buffer.seek(0)

    st.download_button(
        "Download State Analytics Report",
        pdf_buffer,
        f"{state}_{metric}_state_analytics.pdf"
    )