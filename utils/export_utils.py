import io
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def chart_download_button(fig, filename="chart.png"):

    try:
        img = fig.to_image(format="png", scale=2)

        st.download_button(
            "Download Chart",
            img,
            filename
        )

    except Exception:

        st.warning("Chart export not supported in cloud environment.")


def export_chart_to_pdf(fig, title="Chart Report"):

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)

    y = 750

    c.setFont("Helvetica-Bold",16)
    c.drawString(200,y,title)

    y -= 40

    try:
        img = fig.to_image(format="png", scale=2)

        img_buffer = io.BytesIO(img)

        c.drawImage(
            ImageReader(img_buffer),
            50,
            y-300,
            width=500,
            height=300
        )

    except Exception:

        c.drawString(50,y,"Chart preview unavailable in cloud environment")

    c.save()

    pdf_buffer.seek(0)

    st.download_button(
        "Download PDF Report",
        pdf_buffer,
        "chart_report.pdf"
    )