import streamlit as st
from knowledge_base import knowledge_base, medications
from reasoning_engine import forward_chaining, get_medications

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
symptoms_list = [
    "joint_pain", "morning_stiffness", "swelling", "age_50+", "bone_spurs",
    "redness", "fever", "skin_rashes", "eye_inflammation", "back_pain", "stiff_spine"
]
selected_symptoms = st.sidebar.multiselect("Symptoms", symptoms_list)

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
