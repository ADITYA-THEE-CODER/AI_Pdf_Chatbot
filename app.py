import streamlit as st
from pypdf import PdfReader

st.title("AI PDF CHATBOT")
st.write("Upload your PDF here.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("PDF uploaded successfully!")
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    st.text_area("Extracted Text", text[:2000], height=300)
