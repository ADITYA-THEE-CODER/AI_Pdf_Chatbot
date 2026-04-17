import streamlit as st
from pypdf import PdfReader
from groq import Groq

st.set_page_config(page_title="AI PDF Chatbot", page_icon="📄", layout="centered")

# CUSTOM UI DESIGN
st.markdown("""
<style>

/* Full Background */
.stApp {
    background: linear-gradient(135deg, #1a1a40, #3a0ca3, #4361ee, #000000);
    background-attachment: fixed;
}

/* Main Title */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #D8C3A5;
    margin-bottom: 10px;
}

/* Subtitle */
.sub-text {
    text-align: center;
    font-size: 18px;
    color: white;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)

# CUSTOM TITLE
st.markdown('<div class="main-title">📄 AI PDF CHATBOT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Upload your PDF and ask your queries.</div>', unsafe_allow_html=True)

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

    # CHECK IF TEXT EXISTS
    if text.strip() == "":
        st.error("No readable text found in this PDF. Try another PDF.")
        st.stop()

    # LIMIT TEXT SIZE
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
                    Keep it simple and useful.

                    PDF Content:
                    {short_text}
                    """

                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
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

    # QUESTION MODE
    elif option == "Ask Question":

        question = st.text_input("Ask something from the PDF")

        if st.button("Get Answer"):
            with st.spinner("Thinking..."):

                try:
                    prompt = f"""
                    Answer the user's question ONLY using the PDF content below.
                    If the answer is not in the PDF, say:
                    "I could not find that in the PDF."

                    PDF Content:
                    {short_text}

                    Question:
                    {question}
                    """

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
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
