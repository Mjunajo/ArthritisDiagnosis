import streamlit as st
from knowledge_base import knowledge_base, medications
from reasoning_engine import forward_chaining, get_medications

# Project Credit
st.markdown("#### Project by Muhammad Junaid, Hamid Shehzad, and Aneeqa")

# Title
st.title("Arthritis Diagnosis System")

# Instructions
st.markdown(
    """
    ### Instructions:
    1. Select your symptoms from the sidebar.
    2. Click the "Diagnose" button to see the diagnosis and recommended medications.
    """
)

# Symptoms
st.sidebar.title("Select Your Symptoms")
st.sidebar.markdown("#### Categorized Symptoms")

# Categorized Symptoms
joint_symptoms = ["joint_pain", "joint_crackling", "morning_stiffness", "swelling"]
systemic_symptoms = ["fever", "chills", "fatigue", "weight_loss", "night_sweats"]
skin_symptoms = ["skin_rashes", "nail_pitting"]
other_symptoms = ["age_50+", "bone_spurs", "back_pain", "stiff_spine", "eye_inflammation", "abdominal_pain", "diarrhea"]

selected_joint_symptoms = st.sidebar.multiselect("Joint Symptoms", joint_symptoms)
selected_systemic_symptoms = st.sidebar.multiselect("Systemic Symptoms", systemic_symptoms)
selected_skin_symptoms = st.sidebar.multiselect("Skin Symptoms", skin_symptoms)
selected_other_symptoms = st.sidebar.multiselect("Other Symptoms", other_symptoms)

# Collect All Selected Symptoms
selected_symptoms = (
    selected_joint_symptoms +
    selected_systemic_symptoms +
    selected_skin_symptoms +
    selected_other_symptoms
)

# Diagnosis Button
if st.sidebar.button("Diagnose"):
    if not selected_symptoms:
        st.error("Please select at least one symptom!")
    else:
        diagnosis = forward_chaining(knowledge_base, selected_symptoms)
        if diagnosis:
            diagnosis_name = diagnosis[0].replace("_", " ").capitalize()
            st.success(f"Diagnosis: {diagnosis_name}")
            
            meds = get_medications(diagnosis[0], medications)
            if meds:
                st.subheader("Recommended Medications:")
                for med in meds:
                    st.write(f"- {med}")
        else:
            st.warning("No matching diagnosis found. Please consult a doctor.")
