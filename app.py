import streamlit as st

st.title("Kahoot Quiz Generator")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("File uploaded successfully!")
    # More to come here
