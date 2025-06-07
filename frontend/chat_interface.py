from backend.chatbot_engine import query_knowledge_base
from backend.profanity_filter import contains_profanity
from backend.logger import log_chat
import streamlit as st

def chat_interface():
    st.subheader("💬 Chat Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "rerun_flag" not in st.session_state:
        st.session_state.rerun_flag = False  # Dummy flag to trigger rerun

    for chat in st.session_state.chat_history:
        role = "🧑‍💼 You" if chat["sender"] == "user" else "🤖 Assistant"
        st.markdown(f"**{role}:** {chat['message']}")

    user_input = st.text_input("Type your question here:")

    if st.button("Send") and user_input.strip():
        if contains_profanity(user_input):
            st.warning("⚠️ Please avoid using inappropriate language.")
            return

        st.session_state.chat_history.append({"sender": "user", "message": user_input})
        response = query_knowledge_base(user_input)
        st.session_state.chat_history.append({"sender": "bot", "message": response})

        email = st.session_state.get("email", "anonymous")
        log_chat(email, user_input, response)

        # Toggle the flag to trigger rerun
        st.session_state.rerun_flag = not st.session_state.rerun_flag
