# --- app.py ---
import streamlit as st
from frontend.chat_interface import chat_interface
from frontend.document_upload import document_uploader

def main():
    st.set_page_config(page_title="Enterprise AI Assistant")
    st.title("🤖 Enterprise AI Assistant")
    menu = st.sidebar.radio("Menu", ["Chat", "Upload Docs"])
    if menu == "Chat":
        chat_interface()
    else:
        document_uploader()

if __name__ == "__main__":
    main()