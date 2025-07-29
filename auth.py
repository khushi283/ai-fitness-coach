import streamlit as st
import pyrebase
from firebase_config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

def login_page():
    st.title("Login to AI Fitness Coach")

    choice = st.selectbox("Login / Signup", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Sign Up":
        if st.button("Create Account"):
            try:
                auth.create_user_with_email_and_password(email, password)
                st.success("Account created! Login now.")
            except Exception as e:
                st.error(e)

    elif choice == "Login":
        if st.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state['user'] = user
                st.success("Logged in successfully!")
                st.experimental_rerun()  # ⬅️ This is required to show the next screen
            except Exception as e:
                st.error("Login failed. Check your credentials.")

    st.markdown("---")

