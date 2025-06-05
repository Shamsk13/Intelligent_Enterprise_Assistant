import streamlit as st
from backend.otp_manager import send_otp, generate_otp

def login_with_2fa():
    st.subheader("🔐 Login with 2-Factor Authentication")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "otp_sent" not in st.session_state:
        st.session_state.otp_sent = False

    if not st.session_state.otp_sent:
        email = st.text_input("Enter your official email ID:")
        if st.button("Send OTP"):
            otp = generate_otp()
            success = send_otp(email, otp)
            if success:
                st.session_state.otp_sent = True
                st.session_state.otp = otp
                st.session_state.email = email
                st.rerun()  # ✅ GOOD: You already have this
            else:
                st.error("Failed to send OTP. Please try again.")
        return False

    else:
        user_otp = st.text_input("Enter the OTP sent to your email:", type="password")
        if st.button("Verify OTP"):
            if user_otp == st.session_state.otp:
                st.session_state.authenticated = True
                st.success("✅ Logged in successfully!")
                st.rerun()  # ✅ MISSING: This forces rerun to render the tabs
                return True
            else:
                st.error("❌ Invalid OTP. Please try again.")
                return False
        return False
