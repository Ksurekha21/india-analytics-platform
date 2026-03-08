import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
import json
import pdfplumber
from PIL import Image
from docx import Document

st.set_page_config(page_title="AI Data Assistant", layout="wide")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# chatbot content here

st.markdown('</div>', unsafe_allow_html=True)

st.title("🤖 Data AI Assistant")

st.write("How can I help you analyze your data?")

# -----------------------
# GROQ CLIENT
# -----------------------

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -----------------------
# FILE UPLOAD
# -----------------------

uploaded_file = st.file_uploader(
    "Upload file",
    type=["csv","xlsx","pdf","png","jpg","jpeg","txt","docx"]
)

df = None
text_data = None

# -----------------------
# HANDLE FILE TYPES
# -----------------------

if uploaded_file:

    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "csv":
        df = pd.read_csv(uploaded_file)

    elif file_type == "xlsx":
        df = pd.read_excel(uploaded_file)

    elif file_type == "pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            text_data = ""
            for page in pdf.pages:
                text_data += page.extract_text()

    elif file_type in ["png","jpg","jpeg"]:
        image = Image.open(uploaded_file)
        st.image(image)

    elif file_type == "txt":
        text_data = uploaded_file.read().decode()

    elif file_type == "docx":
        doc = Document(uploaded_file)
        text_data = "\n".join([p.text for p in doc.paragraphs])

# -----------------------
# SHOW DATASET
# -----------------------

if df is not None:

    st.subheader("Dataset Preview")

    

# -----------------------
# USER PROMPT
# -----------------------

prompt = st.chat_input("Ask anything about the data")

if prompt:

    st.chat_message("user").write(prompt)

    # -----------------------
    # IF DATASET EXISTS
    # -----------------------

    if df is not None:

        columns = list(df.columns)

        instruction = f"""
You are a data analyst assistant.

Dataset columns:
{columns}

User question:
{prompt}

Determine the intent.

Rules:

1. If the user asks for charts, graphs, plots, visualization → return:

{{
"type":"chart",
"chart":"line/bar/scatter/histogram/pie/area",
"x":"column",
"y":"column"
}}

2. If the user explicitly asks for code → return:

{{
"type":"code",
"code":"python code here"
}}

3. If the user asks a normal question about the dataset → return:

{{
"type":"text",
"answer":"clear explanation"
}}

Return JSON only.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"user","content":instruction}]
        )

        ai_reply = response.choices[0].message.content

        try:
            result = json.loads(ai_reply)
        except:
            result = {"type":"text","answer":ai_reply}

        # -----------------------
        # CREATE CHART
        # -----------------------

        if result["type"] == "chart":

            chart = result["chart"]
            x = result["x"]
            y = result["y"]

            if chart == "line":
                fig = px.line(df,x=x,y=y)

            elif chart == "bar":
                fig = px.bar(df,x=x,y=y)

            elif chart == "scatter":
                fig = px.scatter(df,x=x,y=y)

            elif chart == "histogram":
                fig = px.histogram(df,x=x)
            elif chart == "pie":
                fig = px.pie(df,names=x,values=y)
            elif chart == "area":
                fig = px.area(df,x=x,y=y)
            else:
                st.chat_message("assistant").write("Sorry, I can't create that type of chart.")
                st.stop()

            st.plotly_chart(fig,use_container_width=True)

            st.chat_message("assistant").write("Here is the chart.")

        else:

            st.chat_message("assistant").write(result["answer"])

    # -----------------------
    # IF TEXT DOCUMENT
    # -----------------------

    elif text_data:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                "role":"user",
                "content":f"Document:\n{text_data}\n\nQuestion:{prompt}"
                }
            ]
        )

        answer = response.choices[0].message.content

        st.chat_message("assistant").write(answer)

    # -----------------------
    # GENERAL AI CHAT
    # -----------------------

    else:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"user","content":prompt}]
        )

        answer = response.choices[0].message.content

        st.chat_message("assistant").write(answer)