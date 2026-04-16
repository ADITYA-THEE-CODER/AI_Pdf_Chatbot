import streamlit as st
from pypdf import PdfReader
from groq import Groq

st.set_page_config(page_title="AI PDF Chatbot", page_icon="📄")

st.title("📄 AI PDF CHATBOT")
st.write("Upload your PDF and ask smart questions using Groq AI.")

# API KEY
api_key = st.text_input("Enter Groq API Key", type="password")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if api_key and uploaded_file is not None:

    client = Groq(api_key=api_key)

    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    st.success("PDF uploaded successfully!")

    option = st.selectbox("Choose Action", ["Summary", "Ask Question"])

    # SUMMARY
    if option == "Summary":
        lines = st.number_input(
            "Enter summary length (lines)",
            min_value=1,
            max_value=50,
            value=10
        )

        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):

                prompt = f"""
                Summarize the following PDF in {lines} clear bullet points.

                PDF Content:
                {text}
                """

                response = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                answer = response.choices[0].message.content
                st.subheader("Summary")
                st.write(answer)

    # ASK QUESTION
    elif option == "Ask Question":
        question = st.text_input("Ask something from the PDF")

        if st.button("Get Answer"):
            with st.spinner("Thinking..."):

                prompt = f"""
                Use the PDF content below to answer the user's question.

                PDF Content:
                {text}

                Question:
                {question}
                """

                response = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                answer = response.choices[0].message.content
                st.subheader("Answer")
                st.write(answer)
