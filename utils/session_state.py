# utils/session_state.py

import streamlit as st

def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "otp_sent" not in st.session_state:
        st.session_state.otp_sent = False
    if "email" not in st.session_state:
        st.session_state.email = ""
    if "otp" not in st.session_state:
        st.session_state.otp = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
