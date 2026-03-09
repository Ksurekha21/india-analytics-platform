from numpy import char
import streamlit as st
import pandas as pd
import plotly.express as px
import io
from prophet import Prophet
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from utils.charts import create_chart

st.set_page_config(page_title="Forecasting", layout="wide")

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
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

metric = st.sidebar.selectbox(
    "Metric",
    [c for c in df.columns if c not in ["state","district","year"]]
)

forecast_level = st.sidebar.selectbox(
    "Forecast Level",
    ["National","State","District"]
)

if forecast_level == "State":
    state = st.sidebar.selectbox(
        "Select State",
        sorted(df["state"].unique())
    )

if forecast_level == "District":
    district = st.sidebar.selectbox(
        "Select District",
        sorted(df["district"].unique())
    )

forecast_years = st.sidebar.slider(
    "Forecast Years",
    1,10,5
)

analyze = st.sidebar.button("Analyze")

# -----------------------------
# SELECT DATA
# -----------------------------
if forecast_level == "National":
    data = df

elif forecast_level == "State":
    data = df[df["state"] == state]

else:
    data = df[df["district"] == district]

st.title("Forecasting Analytics")

if analyze:

    # -----------------------------
    # PREPARE DATA
    # -----------------------------
    yearly = data.groupby("year")[metric].mean().reset_index()

    prophet_df = yearly.rename(
        columns={"year":"ds",metric:"y"}
    )

    prophet_df["ds"] = pd.to_datetime(prophet_df["ds"],format="%Y")

    if prophet_df["y"].count() < 2:
        st.error("Not enough data for forecasting.")
        st.stop()

    # -----------------------------
    # TRAIN MODEL
    # -----------------------------
    model = Prophet()

    model.fit(prophet_df)

    future = model.make_future_dataframe(
        periods=forecast_years,
        freq="Y"
    )

    forecast = model.predict(future)

    # -----------------------------
    # FORECAST CHART
    # -----------------------------
    st.header("Forecast Chart")

    fig = px.line(
        forecast,
        x="ds",
        y="yhat",
        labels={"ds":"Year","yhat":metric}
    )

    fig.add_scatter(
        x=forecast["ds"],
        y=forecast["yhat_upper"],
        mode="lines",
        name="Upper Range"
    )

    fig.add_scatter(
        x=forecast["ds"],
        y=forecast["yhat_lower"],
        mode="lines",
        name="Lower Range"
    )

    st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # DOWNLOAD FORECAST CHART
    # -----------------------------
    chart_image = fig.to_image(format="png")

    st.download_button(
        "⬇ Download Chart",
        fig.to_image(format="png"),
        f"{metric}_{chart_image}.png",
        mime="image/png",
        key="download_chart"
        )


    st.header("Forecast Table")

    forecast_table = forecast[["ds","yhat_lower","yhat","yhat_upper"]].copy()

    forecast_table["Year"] = forecast_table["ds"].dt.year

    forecast_table = forecast_table[["Year","yhat_lower","yhat","yhat_upper"]]

    forecast_table.columns = [
    "Year",
    "Lower Range",
    "Predicted",
    "Upper Range"
    ]

    forecast_table = forecast_table.tail(forecast_years)

    st.dataframe(forecast_table,use_container_width=True)

    # -----------------------------
    # PREDICTED INSIGHTS
    # -----------------------------


    
    first = forecast_table.iloc[0]

    
    st.header("Predicted Insights")



    last_value = forecast["yhat"].iloc[-1]
    first_value = forecast["yhat"].iloc[0]

    trend = "increase 📈" if last_value > first_value else "decrease 📉"

    future_year = forecast["ds"].dt.year.iloc[-1]

    if forecast_level == "National":
        entity = "India"

    elif forecast_level == "State":
        entity = state

    else:
        entity = district

    insights = [
        f"The forecast indicates a {trend} in {metric} for {entity}.",
        f"By {future_year}, the predicted value may reach approximately {round(last_value,2)}.",
        f"The predicted range for {future_year} is between {round(first['Lower Range'],2)} and {round(first['Upper Range'],2)}."
        
    ]

    for i in insights:
        st.write("•",i)

    # -----------------------------
    # DOWNLOAD FULL REPORT
    # -----------------------------
    st.header("Download Forecast Report")

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)

    y = 780

    c.setFont("Helvetica-Bold",18)
    c.drawString(150,y,"Forecasting Report")

    y -= 40

    c.setFont("Helvetica",12)
    c.drawString(50,y,f"Sector : {sector}")

    y -= 20
    c.drawString(50,y,f"Metric : {metric}")

    y -= 20
    c.drawString(50,y,f"Forecast Level : {forecast_level}")

    y -= 40

    # Chart title
    c.setFont("Helvetica-Bold",14)
    c.drawString(50,y,"Forecast Chart")

    img_buffer = io.BytesIO(chart_image)

    c.drawImage(
        ImageReader(img_buffer),
        50,
        y-250,
        width=500,
        height=250
    )

    y -= 280



    # -----------------------------
# FORECAST TABLE TITLE
# -----------------------------

    c.showPage()

    c.setFont("Helvetica-Bold",16)
    c.drawString(200,780,"Forecast Table")

    y = 740

    c.setFont("Helvetica",11)

    for i,row in forecast_table.iterrows():

        line = f"{int(row['Year'])} | {round(row['Lower Range'],2)} | {round(row['Predicted'],2)} | {round(row['Upper Range'],2)}"

        c.drawString(60,y,line)

        y -= 20

    c.save()

    pdf_buffer.seek(0)

    st.download_button(
    "Download Forecast Report as PDF",
    pdf_buffer,
    f"{sector}_{forecast_level}_forecast.pdf",
    mime="application/pdf",
    key="download_pdf"
)