import streamlit as st 

st.title("AI PDF CHATBOT")
st.write("Upload your PDF here.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
