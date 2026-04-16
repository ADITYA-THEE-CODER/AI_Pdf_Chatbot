import streamlit as st
from pypdf import PdfReader
from groq import Groq

st.set_page_config(page_title="AI PDF Chatbot", page_icon="📄")

st.title("📄 AI PDF CHATBOT")
st.write("Upload your PDF and ask smart questions using Groq AI.")

# SECRET API KEY
api_key = st.secrets["GROQ_API_KEY"]

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if api_key and uploaded_file is not None:

    client = Groq(api_key=api_key)

    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    # LIMIT TEXT SIZE (important fix)
    short_text = text[:6000]

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
                try:
                    prompt = f"""
                    Summarize the following PDF in {lines} clear bullet points.

                    PDF Content:
                    {short_text}
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

                except Exception as e:
                    st.error("Error while generating summary.")
                    st.write(e)

    # ASK QUESTION
    elif option == "Ask Question":
        question = st.text_input("Ask something from the PDF")

        if st.button("Get Answer"):
            with st.spinner("Thinking..."):
                try:
                    prompt = f"""
                    Use the PDF content below to answer the user's question.

                    PDF Content:
                    {short_text}

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

                except Exception as e:
                    st.error("Error while getting answer.")
                    st.write(e)
