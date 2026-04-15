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

    option = st.selectbox("Choose Action", ["Summary", "Ask Question"])

    if option == "Summary":
        lines = st.number_input("Enter number of summary lines", min_value=1, max_value=200, value=20, step=1)
        st.subheader("Summary")
        summary = text[:lines * 200].split(".")
        for line in summary[:lines]:
            st.write("•", line)
    
    elif option == "Ask Question":
        question = st.text_input("What question do you want to ask?")

