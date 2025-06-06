# --- frontend/document_upload.py ---
import streamlit as st
from backend.document_processor import process_document

def document_uploader():
    st.subheader("📄 Upload Document")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
    if st.button("Upload") and uploaded_file:
        process_document(uploaded_file)
        st.success("Uploaded successfully. Please rebuild knowledge base.")