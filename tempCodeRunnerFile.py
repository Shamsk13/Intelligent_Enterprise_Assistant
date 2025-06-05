import streamlit as st
from frontend.login_2fa import login_with_2fa
from frontend.chat_interface import chat_interface
from frontend.document_upload import document_uploader
from backend.document_processor import process_document



def main():
    st.set_page_config(page_title="Intelligent Enterprise Assistant")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    st.title("🤖 Intelligent Enterprise Assistant")

    if not st.session_state.authenticated:
        login_with_2fa()
    else:
        tab1, tab2 = st.tabs(["📄 Document Upload", "💬 Ask a Question"])
        
        with tab1:
            document_uploader()

        with tab2:
            chat_interface()

if __name__ == "__main__":
    main()

