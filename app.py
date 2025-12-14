import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load your trained model
model_path = r"C:\Users\dell\OneDrive\Documents\Machine Learning\CISWIEProject\asd_RF_pipeline.pkl"
model = joblib.load(model_path)

# Define the M-CHAT questions
questions = {
    "A1": "Does your child look at you when you call his/her name?",
    "A2": "How easy is it for you to get eye contact with your child?",
    "A3": "Does your child point to indicate that s/he wants something? (e.g. a toy that is out of reach)",
    "A4": "Does your child point to share interest with you? (e.g. pointing at an interesting sight)",
    "A5": "Does your child pretend? (e.g. care for dolls, talk on a toy phone)",
    "A6": "Does your child follow where you’re looking?",
    "A7": "If someone is upset, does your child try to comfort them? (e.g. hugging)",
    "A8": "Would you describe your child’s first words as:",
    "A9": "Does your child use simple gestures? (e.g. wave goodbye)",
    "A10": "Does your child stare at nothing with no apparent purpose?"
}

st.title("🧠 ASD Detection Chatbot")
st.write("Answer the questions one by one. The model will predict whether the child may show signs of ASD.")

# Initialize session state
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "done" not in st.session_state:
    st.session_state.done = False

# Step 1: Collect demographic data
if "demographic_done" not in st.session_state:
    st.subheader("👤 Child Information")

    age = st.number_input("Age:", min_value=1, max_value=120, step=1)
    sex = st.selectbox("Sex:", ["m", "f"])
    jaundice = st.selectbox("Jaundice at birth:", ["yes", "no"])
    family_asd = st.selectbox("Family member with ASD:", ["yes", "no"])

    if st.button("Start Test"):
        st.session_state.demographic_done = True
        st.session_state.demographic_data = {
            "Age": age,
            "Sex": sex,
            "Jaundice": jaundice,
            "Family_mem_with_ASD": family_asd
        }
        st.rerun()

# Step 2: Ask M-CHAT questions one by one
elif not st.session_state.done:
    q_keys = list(questions.keys())
    current_key = q_keys[st.session_state.current_q]

    st.subheader(f"Question {st.session_state.current_q + 1}:")
    st.write(questions[current_key])

    answer = st.radio("Your answer:", ["Yes", "No"], key=f"q_{st.session_state.current_q}")

    if st.button("Next"):
        st.session_state.answers[current_key] = 1 if answer == "Yes" else 0

        if st.session_state.current_q + 1 < len(q_keys):
            st.session_state.current_q += 1
            st.rerun()
        else:
            st.session_state.done = True
            st.rerun()

# Step 3: Predict ASD
else:
    st.success("✅ All questions answered! Making prediction...")

    # Calculate the Qchat score automatically
    qchat_score = sum(st.session_state.answers.values())

    st.info(f"📘 Qchat Score Automatically Calculated: **{qchat_score} / 10**")

    # Combine data
    data = st.session_state.answers
    data.update(st.session_state.demographic_data)
    data["Qchat-Score"] = qchat_score

    df = pd.DataFrame([data])

    prediction = model.predict(df)[0]
    label = "ASD" if prediction == 1 else "No ASD"

    st.markdown(f"### 🧾 Prediction Result: **{label}**")

    if label == "ASD":
        st.warning("⚠️ The model suggests possible signs of ASD. Please consult a specialist.")
    else:
        st.success("🎉 The model suggests no ASD risk detected.")

    if st.button("Restart Test"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
