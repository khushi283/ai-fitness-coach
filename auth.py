import streamlit as st
import pyrebase
from firebase_config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

def login_page():
    st.title("Login to AI Fitness Coach")

    # Already logged in
    if 'user' in st.session_state:
        st.info("✅ You are already logged in.")
        return

    choice = st.selectbox("Login / Signup", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # Use separate flags to control rerun
    login_success = False
    signup_success = False
    login_failed = False

    if choice == "Sign Up":
        if st.button("Create Account"):
            try:
                auth.create_user_with_email_and_password(email, password)
                signup_success = True
            except Exception as e:
                st.error(f"❌ {e}")
    else:
        if st.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state['user'] = user
                login_success = True
            except Exception as e:
                login_failed = True

    if signup_success:
        st.success("✅ Account created! Please log in.")
    if login_success:
        st.success("✅ Logged in successfully! Redirecting...")
        st.rerun()
    if login_failed:
        st.error("❌ Login failed. Please check your credentials.")
