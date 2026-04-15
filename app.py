import streamlit as st 

st.title("AI PDF CHATBOT")
st.write("Upload your PDF here.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    st.write("PDF uploaded successfully!")

else:
  st.write("PDF not detected")
