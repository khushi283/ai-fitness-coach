# profile.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin (run only once)
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")  # Place this JSON in your project folder
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ai-fitness-trainer-1c4bf-default-rtdb.firebaseio.com/'
    })

def profile_page(user):
    st.title("📝 Your Fitness Profile")

    # Input form
    with st.form("profile_form"):
        name = st.text_input("Name", max_chars=50)
        age = st.number_input("Age", min_value=10, max_value=100, step=1)
        weight = st.number_input("Weight (in kg)", min_value=20.0, max_value=300.0, step=0.5)
        medical = st.text_area("Medical Conditions", placeholder="E.g. asthma, back pain...")
        diet = st.text_area("Dietary Instructions", placeholder="E.g. vegetarian, high protein...")
        workout_days = st.slider("Workout Days Per Week", 1, 7, 3)
        submit = st.form_submit_button("Save Profile")

    if submit:
        profile_data = {
            "name": name,
            "age": int(age),
            "weight": float(weight),
            "medical_conditions": medical,
            "dietary_instructions": diet,
            "workout_days": int(workout_days)
        }

        # Save to Firebase DB
        try:
            db.reference(f"users/{user['localId']}/profile").set(profile_data)
            st.success("✅ Profile saved successfully!")
        except Exception as e:
            st.error(f"❌ Error saving profile: {e}")

