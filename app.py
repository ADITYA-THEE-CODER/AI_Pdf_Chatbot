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
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    option = st.selectbox("Choose Action", ["Summary", "Ask Question"])

    # SUMMARY FEATURE
    if option == "Summary":
        lines = st.number_input(
            "Enter number of summary lines",
            min_value=1,
            max_value=200,
            value=20,
            step=1
        )

        if st.button("Generate Summary"):
            st.subheader("Summary")

            summary_lines = text.split("\n")

            for line in summary_lines[:lines]:
                if line.strip() != "":
                    st.write("•", line)

    # ASK QUESTION FEATURE
    elif option == "Ask Question":
        question = st.text_input("What question do you want to ask?")

        if question:
            st.subheader("Answer")

            sentences = text.split(".")
            found = False

            for sentence in sentences:
                if question.lower() in sentence.lower():
                    st.write("•", sentence.strip())
                    found = True

            if not found:
                st.warning("No relevant answer found in the PDF.")
