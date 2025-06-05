# frontend/document_upload.py

'''
import streamlit as st
from PyPDF2 import PdfReader
import docx

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def summarize_text(text):
    # Placeholder summary function
    return text[:300] + "..." if len(text) > 300 else text

def document_uploader():
    st.subheader("📄 Upload and Summarize Document")

    uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/docx"]:
            text = extract_text_from_docx(uploaded_file)
        else:
            st.error("Unsupported file type.")
            return

        st.write("### 🔍 Extracted Text Preview:")
        st.text(text[:1000])  # show first 1000 chars

        if st.button("Summarize Document"):
            summary = summarize_text(text)
            st.write("### 📌 Summary:")
            st.success(summary)


'''

# frontend/document_upload.py

import streamlit as st
from backend.document_processor import process_document

def document_uploader():
    st.subheader("📄 Upload and Summarize Document")

    uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

    if uploaded_file:
        st.info("📂 File uploaded. Processing...")

        summary, keywords = process_document(uploaded_file)

        st.write("### 📌 Summary:")
        st.success(summary)

        st.write("### 🗝️ Extracted Keywords:")
        st.code(", ".join(keywords))





from backend.document_processor import process_document, build_knowledge_base

def document_uploader():
    st.subheader("📄 Upload and Summarize Document")

    uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

    if uploaded_file:
        st.info("📂 File uploaded. Processing...")

        summary, keywords = process_document(uploaded_file)

        st.write("### 📌 Summary:")
        st.success(summary)

        st.write("### 🗝️ Extracted Keywords:")
        st.code(", ".join(keywords))

        # 🧠 Build knowledge base
        text = extract_text(uploaded_file)
        chunks = split_text(text)
        build_knowledge_base(chunks)
        st.success("✅ Knowledge base updated!")
